from typing import Optional

import strawberry

from sqlalchemy import select

from src.db.db_conf import db_session
from src.models import library_models
from src.strawberry_types.lsw_types import (
    Book,
    Author,
    AddBookResponse,
    AuthorNotFound,
    AuthorNameMissing,
    AuthorExists,
    AddAuthorResponse,
)

db = db_session.session_factory()


@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        sql = select(library_models.Book).order_by(library_models.Book.title)
        db_books = db.execute(sql).scalars().unique().all()
        return [Book.marshal(book) for book in db_books]

    @strawberry.field
    def authors(self) -> list[Author]:
        sql = select(library_models.Author).order_by(
            library_models.Author.name
        )
        db_authors = db.execute(sql).scalars().unique().all()
        return [Author.marshal(author) for author in db_authors]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(
        self, title: str, author_name: Optional[str]
    ) -> AddBookResponse:
        if author_name:
            sql = select(library_models.Author).where(
                library_models.Author.name == author_name
            )
            db_author = db.execute(sql).scalars().first()
            if not db_author:
                return AuthorNotFound()
        else:
            return AuthorNameMissing()

        db_book = library_models.Book(title=title, author=db_author)
        db.add(db_book)
        db.commit()
        return Book.marshal(db_book)

    @strawberry.mutation
    def add_author(self, name: str) -> AddAuthorResponse:
        sql = select(library_models.Author).where(
            library_models.Author.name == name
        )
        existing_db_author = db.execute(sql).scalars().first()
        if existing_db_author is not None:
            return AuthorExists()
        db_author = library_models.Author(name=name)
        db.add(db_author)
        db.commit()
        return Author.marshal(db_author)


author_schema = strawberry.Schema(query=Query, mutation=Mutation)
