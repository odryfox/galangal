import settings
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig


def migrate_db(database_url: str):
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', database_url)
    alembic_upgrade(alembic_config, 'head')


migrate_db(database_url=settings.DATABASE_URL)
