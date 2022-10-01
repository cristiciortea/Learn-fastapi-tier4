"""Initial migration

Revision ID: fbc8c67da7bc
Revises: ec152f824a00
Create Date: 2022-10-01 20:06:12.940814

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fbc8c67da7bc"
down_revision = "ec152f824a00"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column(
            "time_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_authors_id"), "authors", ["id"], unique=False)
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column(
            "time_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_books_id"), "books", ["id"], unique=False)
    op.drop_index("ix_book_id", table_name="book")
    op.drop_table("book")
    op.drop_table("author")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "author",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('author_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("age", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "time_created",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "time_updated",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="author_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "book",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("rating", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "author_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "time_created",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "time_updated",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"], ["author.id"], name="book_author_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="book_pkey"),
    )
    op.create_index("ix_book_id", "book", ["id"], unique=False)
    op.drop_index(op.f("ix_books_id"), table_name="books")
    op.drop_table("books")
    op.drop_index(op.f("ix_authors_id"), table_name="authors")
    op.drop_table("authors")
    # ### end Alembic commands ###