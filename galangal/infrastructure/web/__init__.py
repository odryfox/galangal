from dependency_injector import containers, providers
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


def create_flask_app(name, bot_url, register_telegram_webhook_usecase, search_phrase_usages_in_different_languages_usecase) -> Flask:
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


class WebContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    telegram_service = providers.Singleton(
        TelegramService,
        token=config.telegram_token,
    )

    regex_language_service = providers.Singleton(RegexLanguageService)

    phrase_usages_in_different_languages_service = providers.Singleton(
        ReversoContextPhraseUsagesInDifferentLanguagesService,
        language_service=regex_language_service,
    )

    register_telegram_webhook_usecase = providers.Singleton(
        RegisterBotWebhookUsecase,
        bot_message_url=config.bot_message_url,
        bot_service=telegram_service,
    )

    search_phrase_usages_in_different_languages_usecase = providers.Singleton(
        SearchPhraseUsagesInDifferentLanguagesUsecase,
        language_service=regex_language_service,
        phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
        bot_service=telegram_service,
    )

    flask_app = providers.Singleton(
        create_flask_app,
        name='web_app',
        bot_url=config.bot_url,
        register_telegram_webhook_usecase=register_telegram_webhook_usecase,
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
    )


def create_app() -> Flask:
    app = WebContainer()

    load_dotenv()

    app.config.telegram_webhook_base_url.from_env('TELEGRAM_WEBHOOK_BASE_URL')
    app.config.telegram_token.from_env('TELEGRAM_TOKEN')
    app.config.bot_url.update('/bot/messages/{}'.format(app.config.telegram_token()))
    app.config.bot_message_url.update('{}/bot/messages/{}'.format(
        app.config.telegram_webhook_base_url(), app.config.telegram_token()
    ))

    return app.flask_app()
