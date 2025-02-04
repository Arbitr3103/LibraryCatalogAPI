from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# ======================================================================
# Схемы для работы с элементами библиотеки
# ======================================================================

class LibraryItemBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    published_year: Optional[int] = None
    description: Optional[str] = None
    available_copies: int = 1  # Значение по умолчанию

    class Config:
        orm_mode = True  # Позволяет работать с объектами SQLAlchemy


class LibraryItemCreate(LibraryItemBase):
    """
    Схема для создания нового элемента библиотеки.
    Использует все поля из LibraryItemBase.
    """
    pass


class LibraryItemRead(LibraryItemBase):
    """
    Схема для чтения (вывода) элемента библиотеки.
    Добавляется поле идентификатора.
    """
    id: int


class LibraryItemUpdate(BaseModel):
    """
    Схема для обновления элемента библиотеки.
    Все поля опциональны.
    """
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    published_year: Optional[int] = None
    description: Optional[str] = None
    available_copies: Optional[int] = None

    class Config:
        orm_mode = True


class LibraryItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    publication_date: Optional[str]
    author: str
    genre: Optional[str]
    available_copies: int
    published_year: Optional[int]

    class Config:
        from_attributes = True  # Поддержка SQLAlchemy моделей


# ======================================================================
# Схемы для работы с пользователями
# ======================================================================

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)  # Минимальная длина пароля
    role: str  # Допустимые значения, например, "admin" или "user"
    is_admin: bool = False

    # Валидатор для проверки сложности пароля (подходит для pydantic v2)
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not any(char.islower() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву.")
        if not any(char.isupper() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        return value


class UserResponse(UserBase):
    id: int
    role: str
    is_admin: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
