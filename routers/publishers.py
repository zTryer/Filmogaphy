from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Publisher
from schemas import PublisherCreate
from typing import List

router = APIRouter(prefix="/publishers", tags=["publishers"])


@router.get("/", response_model=List[PublisherCreate])
def get_publishers(db: Session = Depends(get_db)):
    return db.query(Publisher).all()


@router.post("/", response_model=PublisherCreate)
def create_publisher(publisher: PublisherCreate, db: Session = Depends(get_db)):
    db_publisher = db.query(Publisher).filter(Publisher.name == publisher.name).first()
    if db_publisher:
        raise HTTPException(status_code=400, detail="Publisher already exists")
    new_publisher = Publisher(name=publisher.name, established_year=publisher.established_year)
    db.add(new_publisher)
    db.commit()
    db.refresh(new_publisher)
    return new_publisher
