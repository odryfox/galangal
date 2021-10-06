import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.DEBUG = os.environ.get('DEBUG')
        self.DATABASE_URL = os.environ.get('DATABASE_URL')
        self.DATABASE_TEST_URL = os.environ.get('DATABASE_TEST_URL')
        self.REDIS_URL = os.environ.get('REDIS_URL')
