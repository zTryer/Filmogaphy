from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import BorrowHistory, Book
from schemas import BorrowHistoryResponse
from typing import List

router = APIRouter(prefix="/books", tags=["history"])

@router.get("/{id}/history", response_model=List[BorrowHistoryResponse])
def get_book_history(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.history