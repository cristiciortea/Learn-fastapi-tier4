""" This is the module that allows fields in the table to be inserted into by
the user and to post data to our api.
"""
from pydantic import BaseModel


class BookSchema(BaseModel):
    """What field do we allow the user to modify? title, rating, author_id."""

    title: str
    content: str
