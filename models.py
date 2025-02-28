from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from database import Base


book_genre_association = Table(
    "book_genre_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("genre_id", Integer, ForeignKey("genres.id"))
)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    birthdate = Column(Date)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    publish_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    author = relationship("Author", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    genres = relationship("Genre", secondary=book_genre_association, back_populates="books")
    history = relationship("BorrowHistory", back_populates="book")


class BorrowHistory(Base):
    __tablename__ = "borrow_history"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    borrower_name = Column(String, index=True)
    borrow_date = Column(Date)
    return_date = Column(Date, nullable=True)
    book = relationship("Book", back_populates="history")


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    books = relationship("Book", secondary=book_genre_association, back_populates="genres")


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    established_year = Column(Integer)
    books = relationship("Book", back_populates="publisher")