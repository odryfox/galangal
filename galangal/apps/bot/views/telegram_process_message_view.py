from bot.messengers.telegram.process_message_service import (
    TelegramProcessMessageService
)
from flask import request
from flask.views import MethodView


class TelegramProcessMessageView(MethodView):
    def __init__(
        self,
        telegram_process_message_service: TelegramProcessMessageService,
    ) -> None:
        self.telegram_process_message_service = telegram_process_message_service

        super().__init__()

    def post(self):

        body = request.get_json()
        self.telegram_process_message_service.execute(telegram_request=body)

        return '!'
