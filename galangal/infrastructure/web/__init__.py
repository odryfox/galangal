import os

from flask import Flask

from dotenv import load_dotenv

from domain.usecases.bot_usecases import RegisterWebhookUsecase, SearchUsageCollocationsUsecase
from infrastructure.bot import TelegramService
from infrastructure.external import ReversoContextUsageCollocationsService
from infrastructure.web.views import BotWebhooksView, BotMessagesView


def create_flask_app(name, web_app) -> Flask:
    app = Flask(name)

    add = app.add_url_rule

    views_kwargs = {'web_app': web_app}
    add('/bot/webhooks', view_func=BotWebhooksView.as_view('bot_webhooks', **views_kwargs))
    add(web_app.bot_url, view_func=BotMessagesView.as_view('bot_messages', **views_kwargs))

    return app


class WebApp:
    def __init__(self):
        load_dotenv()

        telegram_webhook_base_url = os.environ['TELEGRAM_WEBHOOK_BASE_URL']
        telegram_token = os.environ['TELEGRAM_TOKEN']

        telegram_service = TelegramService(token=telegram_token)

        self.bot_url = '/bot/messages/{}'.format(telegram_token)
        self.bot_message_url = '{}/bot/messages/{}'.format(telegram_webhook_base_url, telegram_token)

        self.register_webhook_usecase = RegisterWebhookUsecase(
            telegram_service=telegram_service
        )
        self.search_usage_collocations_usecase = SearchUsageCollocationsUsecase(
            usage_collocations_service=ReversoContextUsageCollocationsService(),
            telegram_service=telegram_service
        )

        self.flask_app = create_flask_app('Web app', web_app=self)

    def run(self):
        self.flask_app.run(debug=True)


def create_app() -> WebApp:
    return WebApp()
