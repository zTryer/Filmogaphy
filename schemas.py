from pydantic import BaseModel, Field, field_validator
import datetime
import re
from typing import Optional, List


class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    birthdate: datetime.date

    @classmethod
    def validate_birthdate(cls, birthdate):
        if birthdate > datetime.date.today():
            raise ValueError("Birth date cannot be in the future")
        return birthdate


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: str = Field(..., pattern=r"^(97(8|9))?\d{9}(\d|X)$", min_length=10, max_length=13)
    publish_date: datetime.date
    author_id: int

    @classmethod
    def validate_publish_date(cls, publish_date):
        if publish_date > datetime.date.today():
            raise ValueError("Publish date must be in the past")
        return publish_date


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publish_date: datetime.date
    author_id: int

    class Config:
        from_attributes = True


class BorrowHistoryResponse(BaseModel):
    borrower_name: str
    borrow_date: datetime.date
    return_date: Optional[datetime.date]


class BorrowRequest(BaseModel):
    borrower_name: str
    book_id: int


class ReturnRequest(BaseModel):
    borrower_name: str
    book_id: int


class GenreCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class PublisherCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    established_year: int

    @field_validator("established_year")
    def validate_established_year(cls, established_year):
        current_year = datetime.date.today().year
        if established_year > current_year:
            raise ValueError("Established year must be in the past")
        return established_year