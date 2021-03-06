import os
from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):

    DEBUG = False
    TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
    TELEGRAM_WEBHOOK_BASE_URL = 'localhost:5000'
    REDIS_URL = 'localhost:6543'
    DATABASE_URL = 'localhost:6543'


class EnvironmentConfig(Config):

    DEBUG = os.environ.get('DEBUG', False)
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    TELEGRAM_WEBHOOK_BASE_URL = os.environ.get('TELEGRAM_WEBHOOK_BASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    DATABASE_URL = os.environ.get('DATABASE_URL')


class TestEnvironmentConfig(Config):

    REDIS_URL = os.environ.get('TEST_REDIS_URL')
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
