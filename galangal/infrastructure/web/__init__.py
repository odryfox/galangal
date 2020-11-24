from domain.services import RegexLanguageService
from domain.skills import create_skill_classifier
from flask import Flask
from infrastructure.bot import TelegramService
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from infrastructure.web.config import Config
from infrastructure.web.views import TelegramMessagesView, TelegramWebhooksView
from millet import Agent


def create_app(config: Config) -> Flask:

    regex_language_service = RegexLanguageService()
    telegram_service = TelegramService(token=config.TELEGRAM_TOKEN)

    phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
        language_service=regex_language_service,
    )

    flask_app = Flask('web_app')
    add = flask_app.add_url_rule

    telegram_webhook_path = '/bot/messages/{}'.format(config.TELEGRAM_TOKEN)
    telegram_webhook_url = '{}{}'.format(
        config.TELEGRAM_WEBHOOK_BASE_URL, telegram_webhook_path
    )

    skill_classifier = create_skill_classifier(
        language_service=regex_language_service,
        phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
    )
    agent = Agent(skill_classifier=skill_classifier)

    add(telegram_webhook_path, view_func=TelegramMessagesView.as_view(
        'bot_messages',
        agent=agent,
        telegram_service=telegram_service,
    ))

    add('/bot/webhooks', view_func=TelegramWebhooksView.as_view(
        'bot_webhooks',
        telegram_service=telegram_service,
        telegram_webhook_url=telegram_webhook_url,
    ))

    return flask_app
