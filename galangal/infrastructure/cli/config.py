import os
from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):
    DATABASE_URL = 'localhost:6543'


class EnvironmentConfig(Config):
    DATABASE_URL = os.environ.get('DATABASE_URL')
