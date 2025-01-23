from datetime import date

from pydantic import BaseModel
from typing import Optional


class LibraryItemCreate(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


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
