from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import BorrowHistory, Book
from schemas import BorrowRequest, ReturnRequest
import datetime

router = APIRouter(prefix="/borrow", tags=["borrow"])

MAX_BORROW_LIMIT = 3


@router.post("/")
def borrow_book(request: BorrowRequest, db: Session = Depends(get_db)):
    active_loans = db.query(BorrowHistory).filter(
        BorrowHistory.borrower_name == request.borrower_name,
        BorrowHistory.return_date == None
    ).count()

    if active_loans >= MAX_BORROW_LIMIT:
        raise HTTPException(status_code=400, detail="Borrower has reached the maximum limit of borrowed books")

    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    existing_borrow = db.query(BorrowHistory).filter(
        BorrowHistory.book_id == request.book_id,
        BorrowHistory.return_date == None
    ).first()

    if existing_borrow:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    new_borrow = BorrowHistory(
        book_id=request.book_id,
        borrower_name=request.borrower_name,
        borrow_date=datetime.date.today()
    )

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return {"message": "Book borrowed successfully"}


@router.post("/return")
def return_book(request: ReturnRequest, db: Session = Depends(get_db)):
    borrow_record = db.query(BorrowHistory).filter(
        BorrowHistory.book_id == request.book_id,
        BorrowHistory.borrower_name == request.borrower_name,
        BorrowHistory.return_date == None
    ).first()

    if not borrow_record:
        raise HTTPException(status_code=400, detail="No active borrow record found for this book and borrower")

    borrow_record.return_date = datetime.date.today()
    db.commit()
    return {"message": "Book returned successfully"}