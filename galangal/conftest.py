import pytest
import settings
from db.connection import Session
from db.utils import migrate_db, truncate_all
from redis import Redis
from redis_client import redis_client
from sqlalchemy_utils import create_database, database_exists, drop_database


@pytest.fixture(scope='session', autouse=True)
def db():
    database_url = settings.DATABASE_URL

    if database_exists(database_url):
        drop_database(database_url)

    create_database(database_url)
    migrate_db()

    yield

    drop_database(database_url)


@pytest.fixture(scope='function', autouse=True)
def session(db):
    truncate_all()
    session = Session()

    yield session

    session.close()


@pytest.fixture(scope='function', autouse=True)
def redis() -> Redis:
    redis_client.flushdb()

    yield redis_client
