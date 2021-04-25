import os
from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):

    REDIS_URL = 'localhost:6543'
    DATABASE_URL = 'localhost:6543'


class EnvironmentConfig(Config):

    REDIS_URL = os.environ.get('REDIS_URL')
    DATABASE_URL = os.environ.get('DATABASE_URL')
