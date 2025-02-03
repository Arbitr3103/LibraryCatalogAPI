from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import LibraryItem, User
from app.schemas import LibraryItemRead, LibraryItemCreate, LibraryItemUpdate
from app.database import get_db
from app.auth import get_current_user

library_router = APIRouter(prefix="/library_items", tags=["Library Items"])


@library_router.post("/", response_model=LibraryItemRead)
def create_library_item(
        item: LibraryItemCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    db_item = LibraryItem(**item.dict())
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating item")


@library_router.get("/", response_model=List[LibraryItemRead])
def get_library_items(
        skip: int = 0,
        limit: int = 10,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        published_year: Optional[int] = None,
        db: Session = Depends(get_db)
):
    query = db.query(LibraryItem)
    if author:
        query = query.filter(LibraryItem.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(LibraryItem.genre.ilike(f"%{genre}%"))
    if published_year:
        query = query.filter(LibraryItem.published_year == published_year)
    return query.offset(skip).limit(limit).all()


@library_router.get("/{item_id}", response_model=LibraryItemRead)
def get_library_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(LibraryItem).filter(LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")
    return db_item


@library_router.put("/{item_id}", response_model=LibraryItemRead)
def update_library_item(
        item_id: int,
        item_update: LibraryItemUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    db_item = db.query(LibraryItem).filter(LibraryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Library item not found")
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@library_router.delete("/{item_id}", response_model=dict)
def delete_library_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
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
