import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from config import Config
from db.connection import DB
from redis import Redis
from sqlalchemy_utils import create_database, database_exists, drop_database


def migrate_db(database_url: str):
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', database_url)
    alembic_upgrade(alembic_config, 'head')


@pytest.fixture(scope='session', autouse=True)
def db():
    config = Config()
    database_url = config.DATABASE_TEST_URL

    if database_exists(database_url):
        drop_database(database_url)

    create_database(database_url)
    migrate_db(database_url)

    yield DB(url=database_url)

    drop_database(database_url)


@pytest.fixture(scope='function', autouse=True)
def session(db: DB):
    connection = db.engine.connect()
    trans = connection.begin()
    session = db.create_session()

    yield session

    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope='function', autouse=True)
def redis() -> Redis:
    config = Config()
    redis = Redis.from_url(url=config.REDIS_TEST_URL)

    redis.flushdb()

    yield redis
