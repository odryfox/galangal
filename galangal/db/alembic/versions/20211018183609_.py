"""

Revision ID: 20211018183609
Revises: 
Create Date: 2021-10-18 18:36:09.451474

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20211018183609'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_id')
    )
    op.create_table('phrases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('source_language_phrase', sa.String(), nullable=False),
    sa.Column('target_language_phrase', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('source_language_phrase'),
    sa.UniqueConstraint('target_language_phrase')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phrases')
    op.drop_table('accounts')
    # ### end Alembic commands ###
