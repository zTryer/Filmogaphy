from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import datetime
from database import get_db
from models import Book, Author
from schemas import BookCreate, BookResponse
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    author = db.query(Author).filter(Author.id == book.author_id).first()

    errors = []
    if existing_book:
        errors.append("ISBN already exists")
    if not author:
        errors.append("Author not found")
    if book.publish_date > datetime.date.today():
        errors.append("Publish date must be in the past")

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    new_book = Book(title=book.title, isbn=book.isbn, publish_date=book.publish_date, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=List[BookResponse])
def get_books(
        db: Session = Depends(get_db),
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        sort_by: Optional[str] = Query(None, pattern="^(title|author|publish_date)$"),
        order: str = Query("asc", pattern="^(asc|desc)$")
):
    query = db.query(Book)

    if sort_by:
        if sort_by == "title":
            query = query.order_by(Book.title.asc() if order == "asc" else Book.title.desc())
        elif sort_by == "author":
            query = query.join(Author).order_by(Author.name.asc() if order == "asc" else Author.name.desc())
        elif sort_by == "publish_date":
            query = query.order_by(Book.publish_date.asc() if order == "asc" else Book.publish_date.desc())

    books = query.offset(offset).limit(limit).all()
    return books