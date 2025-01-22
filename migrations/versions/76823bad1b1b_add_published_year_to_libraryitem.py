"""Add published_year to LibraryItem

Revision ID: 76823bad1b1b
Revises: 
Create Date: 2025-01-21 21:22:33.450853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76823bad1b1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_books_id', table_name='books')
    op.drop_index('ix_books_title', table_name='books')
    op.drop_table('books')
    op.drop_index('ix_library_items_id', table_name='library_items')
    op.drop_index('ix_library_items_title', table_name='library_items')
    op.drop_table('library_items')
    op.drop_index('ix_authors_id', table_name='authors')
    op.drop_index('ix_authors_name', table_name='authors')
    op.drop_table('authors')
    op.drop_index('ix_readers_id', table_name='readers')
    op.drop_table('readers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('registration_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='readers_pkey')
    )
    op.create_index('ix_readers_id', 'readers', ['id'], unique=False)
    op.create_table('authors',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('authors_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('biography', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('birth_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='authors_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_authors_name', 'authors', ['name'], unique=False)
    op.create_index('ix_authors_id', 'authors', ['id'], unique=False)
    op.create_table('library_items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('publication_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('available_copies', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='library_items_pkey')
    )
    op.create_index('ix_library_items_title', 'library_items', ['title'], unique=False)
    op.create_index('ix_library_items_id', 'library_items', ['id'], unique=False)
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('publish_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('available_copies', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], name='books_author_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='books_pkey')
    )
    op.create_index('ix_books_title', 'books', ['title'], unique=False)
    op.create_index('ix_books_id', 'books', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
