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
