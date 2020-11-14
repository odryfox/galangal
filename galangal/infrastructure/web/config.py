import os
from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):

    TELEGRAM_TOKEN = ''
    TELEGRAM_WEBHOOK_BASE_URL = ''
    BOT_URL = ''
    BOT_MESSAGE_URL = ''


class EnvironmentConfig(Config):

    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    TELEGRAM_WEBHOOK_BASE_URL = os.environ['TELEGRAM_WEBHOOK_BASE_URL']
    BOT_URL = '/bot/messages/{}'.format(TELEGRAM_TOKEN)
    BOT_MESSAGE_URL = '{}/bot/messages/{}'.format(
        TELEGRAM_WEBHOOK_BASE_URL, TELEGRAM_TOKEN
    )
