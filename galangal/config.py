import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.environ.get('DEBUG')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_TEST_URL = os.environ.get('DATABASE_TEST_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
