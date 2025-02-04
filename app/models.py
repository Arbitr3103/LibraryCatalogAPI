# app/models.py
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base  # Импортируем Base из database.py


# Модель для авторов
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    biography = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author")


# Модель для книг
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    published_year = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    genre = Column(String, nullable=True)
    available_copies = Column(Integer, default=1)

    author = relationship("Author", back_populates="books")


# Модель для читателей
class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    registration_date = Column(Date, nullable=True)

    borrowed_books = relationship("BorrowedBook", back_populates="reader")


# Модель для записей о взятых книгах
class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    reader = relationship("Reader", back_populates="borrowed_books")
    book = relationship("Book")


# Модель для элементов библиотеки
class LibraryItem(Base):
    """
    Модель для элементов библиотеки. Может использоваться для сохранения старого функционала.
    """
    __tablename__ = 'library_items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    published_year = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    available_copies = Column(Integer, nullable=False, default=1)


# Модель для пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_admin = Column(Boolean, default=False)
