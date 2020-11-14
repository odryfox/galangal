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


def create_flask_app(name, web_app) -> Flask:
    app = Flask(name)

    add = app.add_url_rule

    views_kwargs = {'web_app': web_app}
    add('/bot/webhooks', view_func=TelegramWebhooksView.as_view('bot_webhooks', **views_kwargs))
    add(web_app.bot_url, view_func=TelegramMessagesView.as_view('bot_messages', **views_kwargs))

    return app


class WebApp:
    def __init__(self):
        load_dotenv()

        telegram_webhook_base_url = os.environ['TELEGRAM_WEBHOOK_BASE_URL']
        telegram_token = os.environ['TELEGRAM_TOKEN']

        telegram_service = TelegramService(token=telegram_token)

        self.bot_url = '/bot/messages/{}'.format(telegram_token)
        self.bot_message_url = '{}/bot/messages/{}'.format(telegram_webhook_base_url, telegram_token)

        self.register_telegram_webhook_usecase = RegisterBotWebhookUsecase(
            bot_service=telegram_service
        )
        self.search_phrase_usages_in_different_languages_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
            language_service=RegexLanguageService(),
            phrase_usages_in_different_languages_service=ReversoContextPhraseUsagesInDifferentLanguagesService(
                language_service=RegexLanguageService()
            ),
            bot_service=telegram_service
        )

        self.flask_app = create_flask_app('Web app', web_app=self)

    def run(self):
        self.flask_app.run(debug=True)


def create_app() -> WebApp:
    return WebApp()
