from domain.usecases.bot_usecases import RegisterBotWebhookUsecase
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from flask import Flask
from infrastructure.bot import TelegramService
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from infrastructure.services import RegexLanguageService
from infrastructure.web.config import Config
from infrastructure.web.views import TelegramMessagesView, TelegramWebhooksView


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


def create_app(config: Config) -> Flask:
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

    flask_app = _create_flask_app(
        name='web_app',
        bot_url=config.BOT_URL,
        register_telegram_webhook_usecase=register_telegram_webhook_usecase,
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
    )
    return flask_app
