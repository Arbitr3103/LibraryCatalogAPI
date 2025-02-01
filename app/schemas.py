from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class LibraryItemCreate(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)  # Минимальная длина пароля

    # Валидатор для проверки сложности пароля
    @field_validator("password")
    def validate_password(cls, value):
        if not any(char.islower() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву.")
        if not any(char.isupper() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        return value


class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LibraryItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    publication_date: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    available_copies: int
    published_year: Optional[int] = None

    class Config:
        orm_mode = True


class LibraryItemRead(BaseModel):
    id: int
    title: str
    author: str
    published_year: Optional[int] = None
    description: Optional[str] = None
    publication_date: Optional[date] = None
    genre: Optional[str] = None
    available_copies: int

    class Config:
        orm_mode = True


class LibraryItemUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    description: Optional[str] = None
    publication_date: Optional[str] = None
    genre: Optional[str] = None
    available_copies: Optional[int] = None

class LibraryItemResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    published_year: Optional[int] = None

    class Config:
        from_attributes = True  # Позволяет Pydantic работать с SQLAlchemy-моделями
