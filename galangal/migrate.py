from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from infrastructure.web.config import EnvironmentConfig


def migrate_db(database_url: str):
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', database_url)
    alembic_upgrade(alembic_config, 'head')


config = EnvironmentConfig()
migrate_db(database_url=config.DATABASE_URL)
