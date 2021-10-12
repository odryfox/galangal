import os


class Config:
    DEBUG = True
    DATABASE_URL = 'postgresql://postgres:pass@postgres_test:5432/galangal'
    REDIS_URL = 'redis://:pass@redis_test:6379/0'
    TELEGRAM_WEBHOOK_BASE_URL = 'https://abcdef123456.ngrok.io'
    TELEGRAM_TOKEN = '1234567890:ABCDEFGH-abcdefghijklmnopqrstuvwxyz'


class EnvironmentConfig(Config):
    DEBUG = os.environ.get('DEBUG')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    TELEGRAM_WEBHOOK_BASE_URL = os.environ.get(
        'TELEGRAM_WEBHOOK_BASE_URL'
    )
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')


class EnvironmentTestConfig(Config):
    DEBUG = os.environ.get('DEBUG')
    DATABASE_URL = os.environ.get('DATABASE_TEST_URL')
    REDIS_URL = os.environ.get('REDIS_TEST_URL')
    TELEGRAM_WEBHOOK_BASE_URL = 'https://abcdef123456.ngrok.io'
    TELEGRAM_TOKEN = '1234567890:ABCDEFGH-abcdefghijklmnopqrstuvwxyz'
