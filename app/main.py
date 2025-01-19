from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, LibraryItem
from app.schemas import LibraryItemCreate
from sqlalchemy.exc import SQLAlchemyError

# Строка подключения к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql://vladimirbragin:Mark2022@localhost/library_catalog"

# Создаем движок для работы с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Инициализация приложения FastAPI
app = FastAPI()


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
