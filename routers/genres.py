from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Genre
from schemas import GenreCreate
from typing import List

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=List[GenreCreate])
def get_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@router.post("/", response_model=GenreCreate)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = db.query(Genre).filter(Genre.name == genre.name).first()
    if db_genre:
        raise HTTPException(status_code=400, detail="Genre already exists")
    new_genre = Genre(name=genre.name)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre