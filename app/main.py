from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, LibraryItem
from app.schemas import LibraryItemCreate, LibraryItemRead
from sqlalchemy.exc import SQLAlchemyError
from app.auth import auth_router
from app.auth import register_user, authenticate_user, create_access_token
from app.schemas import UserCreate, UserLogin
from decouple import config
from typing import List
from . import models, schemas
from .database import get_db

# Строка подключения к базе данных
SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

# Создаем движок для работы с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Инициализация приложения FastAPI
app = FastAPI()

# Подключение маршрутов авторизации
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


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
@app.post("/library_item/")
def create_library_item(item: LibraryItemCreate, db: Session = Depends(get_db)):
    db_item = LibraryItem(title=item.title, author=item.author, published_year=item.published_year)
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating item")


# Получить все элементы из каталога
@app.get("/library_items/")
def get_library_items(db: Session = Depends(get_db)):
    items = db.query(LibraryItem).all()
    return items


@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/library_items/", response_model=List[schemas.LibraryItem])
def get_library_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Получить список элементов библиотеки.
    :param skip: Количество элементов, которые нужно пропустить (для пагинации).
    :param limit: Максимальное количество элементов для возвращения.
    :param db: Сессия базы данных.
    :return: Список элементов библиотеки.
    """
    items = db.query(models.LibraryItem).offset(skip).limit(limit).all()
    return items


@app.get("/library_item/{item_id}", response_model=LibraryItemRead)
def get_library_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(LibraryItem).filter(LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")
    return db_item


@app.put("/library_item/{item_id}", response_model=schemas.LibraryItem)
def update_library_item(item_id: int, item_update: schemas.LibraryItemUpdate, db: Session = Depends(get_db)):
    # Получаем элемент из базы данных
    db_item = db.query(models.LibraryItem).filter(models.LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")

    # Обновляем только те поля, которые были переданы в запросе
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Сохраняем изменения в базе данных
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
