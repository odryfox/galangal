import enum

import settings


class ActionType(enum.Enum):
    GREETING = 'greeting'
    ADD_PHRASE_TO_STUDY = 'add_phrase_to_study'


TELEGRAM_WEBHOOK_PATH = '/bot/messages/{}'.format(settings.TELEGRAM_TOKEN)
