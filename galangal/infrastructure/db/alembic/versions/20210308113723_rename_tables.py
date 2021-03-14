"""Rename tables

Revision ID: 20210308113723
Revises: 20210104182024
Create Date: 2021-03-08 11:37:24.190092

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20210308113723'
down_revision = '20210104182024'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('phrase_links', 'synonyms')
    op.rename_table('study_phrases', 'study_synonyms')

    op.drop_constraint('account_link_unique', 'study_synonyms')
    op.alter_column('study_synonyms', 'link_id', nullable=False, new_column_name='synonym_id')
    op.create_unique_constraint('account_synonym_unique', 'study_synonyms', ['account_id', 'synonym_id'])


def downgrade():
    op.drop_constraint('account_synonym_unique', 'study_synonyms')
    op.alter_column('study_synonyms', 'synonym_id', nullable=False, new_column_name='link_id')
    op.create_unique_constraint('account_link_unique', 'study_synonyms', ['account_id', 'link_id'])

    op.rename_table('study_synonyms', 'study_phrases')
    op.rename_table('synonyms', 'phrase_links')
