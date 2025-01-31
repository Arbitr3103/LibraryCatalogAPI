from typing import List, Optional
from decouple import config
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session

from app.auth import auth_router, register_user, authenticate_user, create_access_token
from app.models import Base, LibraryItem
from app.schemas import LibraryItemCreate, LibraryItemRead, UserCreate, UserLogin, LibraryItemUpdate
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Строка подключения к базе данных
SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

# Создаем движок для работы с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Инициализация приложения FastAPI
app = FastAPI()

# Инициализация маршрутизатора
router = APIRouter()

# Подключение маршрутов авторизации
app.include_router(auth_router)


# Функция для создания всех таблиц
def create_db():
    Base.metadata.create_all(bind=engine)


# Создаем таблицы при запуске приложения
create_db()


# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Главная страница API
@app.get("/")
def read_root():
    return {"message": "Library Catalog API is up and running"}


# Создание нового элемента в каталоге
@app.post("/library_item/", response_model=LibraryItemRead)
def create_library_item(item: LibraryItemCreate, db: Session = Depends(get_db)):
    db_item = LibraryItem(title=item.title, author=item.author, published_year=item.published_year)
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating item")


# Получить элементы из каталога с фильтрацией
@app.get("/library_items/", response_model=List[LibraryItemRead])
def get_library_items(
    skip: int = 0,
    limit: int = 10,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    published_year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Получить список элементов библиотеки с возможностью фильтрации и пагинации.
    """
    query = db.query(LibraryItem)

    # Фильтрация по автору, жанру и году публикации
    if author:
        query = query.filter(LibraryItem.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(LibraryItem.genre.ilike(f"%{genre}%"))
    if published_year:
        query = query.filter(LibraryItem.published_year == published_year)

    # Пагинация
    return query.offset(skip).limit(limit).all()


# Получение элемента по ID
@app.get("/library_item/{item_id}", response_model=LibraryItemRead)
def get_library_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(LibraryItem).filter(LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")
    return db_item


# Обновление элемента
@app.put("/library_item/{item_id}", response_model=LibraryItemRead)
def update_library_item(item_id: int, item_update: LibraryItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(LibraryItem).filter(LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")

    # Обновляем только переданные поля
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


# Удаление элемента
@app.delete("/library_items/{item_id}", response_model=dict)
def delete_library_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(LibraryItem).filter(LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")
    try:
        db.delete(db_item)
        db.commit()
        return {"detail": "Item deleted successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete item")
