import os
import pathlib

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from src.models.library_models import Book, Author
from src.schemas.library_post_schemas import BookSchema, AuthorSchema

# Define environment variables for customization of alembic
BASE_DIR = pathlib.Path(__file__).absolute().parent.parent
load_dotenv(BASE_DIR / ".env")

# Create FastAPI instance
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


# Define api endpoints
@app.get("/")
async def root():
    return {
        "message": "Hello to my fastapi world! Nothing to see here, try using /docs"
    }


@app.post("/add-book/", response_model=BookSchema)
def add_book(book: BookSchema):
    db_book = Book(
        title=book.title, rating=book.rating, author_id=book.author_id
    )
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/add-author/", response_model=AuthorSchema)
def add_author(author: AuthorSchema):
    db_author = Author(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.get("/books/")
def get_books():
    books = db.session.query(Book).all()
    return books


if (
    __name__ == "__main__"
):  # this is to be able to run the api on local machine, no docker containers
    uvicorn.run(app, host="0.0.0.0", port=8000)
