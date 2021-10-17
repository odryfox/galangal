import sys
from datetime import datetime

import settings
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig


def migrate_db():
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    alembic_upgrade(alembic_config, 'head')


def make_migration_db() -> None:
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    now = datetime.now()
    now_str = now.strftime('%Y%m%d%H%M%S')

    try:
        message_index = sys.argv.index('-m') + 1
        message = sys.argv[message_index]
    except (ValueError, IndexError):
        message = ''

    alembic_revision(
        alembic_config,
        message=message,
        autogenerate=True,
        rev_id=now_str,
    )
