from fastapi import FastAPI
from database import engine, Base
from routers import authors, books, history, borrow, genres, publishers


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(authors.router)
app.include_router(books.router)
app.include_router(history.router)
app.include_router(borrow.router)
app.include_router(genres.router)
app.include_router(publishers.router)