from flask import request
from flask.views import MethodView
from infrastructure.bot.telegram import TelegramBot
from millet import Agent


class TelegramWebhooksView(MethodView):
    def __init__(
        self,
        telegram_bot: TelegramBot,
        telegram_webhook_url: str,
    ) -> None:
        self._telegram_bot = telegram_bot
        self._telegram_webhook_url = telegram_webhook_url

        super().__init__()

    def get(self):
        self._telegram_bot.register_webhook(self._telegram_webhook_url)
        return '!'


class TelegramMessagesView(MethodView):
    def __init__(
        self,
        agent: Agent,
        telegram_bot: TelegramBot,
    ):
        self._agent = agent
        self._telegram_bot = telegram_bot

        super().__init__()

    def post(self):

        body = request.get_json()
        user_request, chat_id = self._telegram_bot.parse_request(body=body)

        responses = self._agent.query(
            user_request,
            chat_id,
        )

        self._telegram_bot.send_responses(responses, chat_id)

        return '!'
