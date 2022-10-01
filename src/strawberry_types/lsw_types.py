from typing import Optional

import strawberry
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from strawberry.types import Info

from src.db.db_conf import db_session
from src.models import library_models

db = db_session.session_factory()


@strawberry.type
class Author:
    id: strawberry.ID
    name: str

    def books(self, info: Info) -> list[library_models.Book]:
        books = info.context["books_by_author"].load(self.id)
        return [Book.marshal(book) for book in books]

    @classmethod
    def marshal(cls, model: library_models.Author) -> "Author":
        return cls(id=strawberry.ID(str(model.id)), name=model.name)


@strawberry.type
class Book:
    id: strawberry.ID
    title: str
    author: Optional[Author] = None

    @classmethod
    def marshal(cls, model: library_models.Book) -> "Book":
        return cls(
            id=strawberry.ID(str(model.id)),
            title=model.title,
            author=Author.marshal(model.author) if model.author else None,
        )


@strawberry.type
class AuthorExists:
    message: str = "Author with this name already exists"


@strawberry.type
class AuthorNotFound:
    message: str = "Couldn't find an author with the supplied name"


@strawberry.type
class AuthorNameMissing:
    message: str = "Please supply an author name"


AddBookResponse = strawberry.union(
    "AddBookResponse", (Book, AuthorNotFound, AuthorNameMissing)
)
AddAuthorResponse = strawberry.union(
    "AddAuthorResponse", (Author, AuthorExists)
)


def load_books_by_author(keys: list) -> list[Book]:
    all_queries = [
        select(library_models.Book).where(library_models.Book.author_id == key)
        for key in keys
    ]
    data = [db.execute(sql).scalars().unique().all() for sql in all_queries]
    print(keys, data)
    return data


def get_context() -> dict:
    return {
        "books_by_author": DataLoader(load_fn=load_books_by_author),
    }
