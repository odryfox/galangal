import sys
from datetime import datetime

import config
from alembic.command import revision as alembic_revision
from alembic.config import Config as AlembicConfig


def make_migration_db(database_url: str) -> None:
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', database_url)
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


make_migration_db(database_url=config.DATABASE_URL)
