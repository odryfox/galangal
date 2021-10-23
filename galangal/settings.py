import os

DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
DATABASE_URL = os.environ.get('DATABASE_URL')
REDIS_URL = os.environ.get('REDIS_URL')
TELEGRAM_WEBHOOK_BASE_URL = os.environ.get('TELEGRAM_WEBHOOK_BASE_URL')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
