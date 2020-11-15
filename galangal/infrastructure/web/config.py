import os
from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):

    TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
    TELEGRAM_WEBHOOK_BASE_URL = 'localhost:5000'


class EnvironmentConfig(Config):

    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    TELEGRAM_WEBHOOK_BASE_URL = os.environ['TELEGRAM_WEBHOOK_BASE_URL']
