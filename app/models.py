from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(Text)
    birth_date = Column(Date)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    publish_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre = Column(String)
    available_copies = Column(Integer, default=1)

    author = relationship("Author", back_populates="books")


class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    registration_date = Column(Date)


class LibraryItem(Base):
    __tablename__ = "library_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    publication_date = Column(Date)
    author = Column(String)
    genre = Column(String)
    available_copies = Column(Integer, default=0)
    published_year = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # Уникальный логин
    email = Column(String, unique=True, index=True, nullable=False)  # Уникальный email
    hashed_password = Column(String, nullable=False)  # Хэш пароля
    is_admin = Column(Boolean, default=False)  # Флаг администратора
