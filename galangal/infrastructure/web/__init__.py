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


def create_app(config: Config) -> Flask:

    regex_language_service = RegexLanguageService()
    telegram_service = TelegramService(token=config.TELEGRAM_TOKEN)

    phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
        language_service=regex_language_service,
    )

    search_phrase_usages_in_different_languages_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
        language_service=regex_language_service,
        phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
        bot_service=telegram_service,
    )

    flask_app = Flask('web_app')
    add = flask_app.add_url_rule

    telegram_webhook_path = '/bot/messages/{}'.format(config.TELEGRAM_TOKEN)
    telegram_webhook_url = '{}{}'.format(
        config.TELEGRAM_WEBHOOK_BASE_URL, telegram_webhook_path
    )

    add(telegram_webhook_path, view_func=TelegramMessagesView.as_view(
        'bot_messages',
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
    ))

    register_telegram_webhook_usecase = RegisterBotWebhookUsecase(
        bot_webhook_url=telegram_webhook_url,
        bot_service=telegram_service,
    )

    add('/bot/webhooks', view_func=TelegramWebhooksView.as_view(
        'bot_webhooks',
        register_telegram_webhook_usecase=register_telegram_webhook_usecase,
    ))

    return flask_app
