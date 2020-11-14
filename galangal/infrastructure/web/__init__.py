import os

from domain.usecases.bot_usecases import RegisterBotWebhookUsecase
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from dotenv import load_dotenv
from flask import Flask
from infrastructure.bot import TelegramService
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from infrastructure.services import RegexLanguageService
from infrastructure.web.views import TelegramMessagesView, TelegramWebhooksView

load_dotenv()


def _create_flask_app(
    name: str,
    bot_url: str,
    register_telegram_webhook_usecase: RegisterBotWebhookUsecase,
    search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
) -> Flask:

    app = Flask(name)
    add = app.add_url_rule

    add('/bot/webhooks', view_func=TelegramWebhooksView.as_view(
        'bot_webhooks',
        register_telegram_webhook_usecase=register_telegram_webhook_usecase,
    ))
    add(bot_url, view_func=TelegramMessagesView.as_view(
        'bot_messages',
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
    ))

    return app


class EnvironmentConfig:
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    TELEGRAM_WEBHOOK_BASE_URL = os.environ['TELEGRAM_WEBHOOK_BASE_URL']
    BOT_URL = '/bot/messages/{}'.format(TELEGRAM_TOKEN)
    BOT_MESSAGE_URL = '{}/bot/messages/{}'.format(
        TELEGRAM_WEBHOOK_BASE_URL, TELEGRAM_TOKEN
    )


class WebApp:

    def __init__(self, config: EnvironmentConfig):
        telegram_service = TelegramService(
            token=config.TELEGRAM_TOKEN,
        )

        regex_language_service = RegexLanguageService()

        phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
            language_service=regex_language_service,
        )

        register_telegram_webhook_usecase = RegisterBotWebhookUsecase(
            bot_message_url=config.BOT_MESSAGE_URL,
            bot_service=telegram_service,
        )

        search_phrase_usages_in_different_languages_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
            language_service=regex_language_service,
            phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
            bot_service=telegram_service,
        )

        self.flask_app = _create_flask_app(
            name='web_app',
            bot_url=config.BOT_URL,
            register_telegram_webhook_usecase=register_telegram_webhook_usecase,
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        )


def create_app() -> Flask:
    environment_config = EnvironmentConfig()
    app = WebApp(config=environment_config)
    return app.flask_app
