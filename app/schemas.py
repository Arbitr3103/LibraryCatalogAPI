from pydantic import BaseModel
from typing import Optional


class LibraryItemCreate(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None

    class Config:
        orm_mode = True
