from flask import Response, request
from flask.views import MethodView
from infrastructure.telegram.bot import TelegramBot


class TelegramWebhooksView(MethodView):
    def __init__(
        self,
        telegram_bot: TelegramBot,
        telegram_webhook_url: str,
    ) -> None:
        self.telegram_bot = telegram_bot
        self.telegram_webhook_url = telegram_webhook_url

        super().__init__()

    def get(self):
        self.telegram_bot.register_webhook(self.telegram_webhook_url)
        return '!'


class TelegramMessagesView(MethodView):
    def __init__(
        self,
        telegram_bot: TelegramBot,
    ) -> None:
        self.telegram_bot = telegram_bot

        super().__init__()

    def post(self):

        body = request.get_json()
        self.telegram_bot.process_request(request=body)

        return '!'


class HealthCheckView(MethodView):

    def get(self):
        return Response(status=200)
