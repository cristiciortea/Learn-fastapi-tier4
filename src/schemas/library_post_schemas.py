""" This is the module that allows fields in the table to be posted by
the user to post data to our api.
"""
from pydantic import BaseModel


class BookSchema(BaseModel):
    """What field do we allow the user to modify? title, rating, author_id."""

    title: str
    rating: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorSchema(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True
