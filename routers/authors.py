from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Author
from schemas import AuthorCreate
import datetime

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/", response_model=AuthorCreate)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.name == author.name).first()
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    if author.birthdate > datetime.date.today():
        raise HTTPException(status_code=400, detail="Birthdate cannot be in the future")
    new_author = Author(name=author.name, birthdate=author.birthdate)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author