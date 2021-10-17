from bot.daos import CallbackDataDAO
from bot.messengers.telegram.process_message_service import (
    TelegramProcessMessageService
)
from flask import request
from flask.views import MethodView


class TelegramProcessMessageView(MethodView):

    def post(self):

        body = request.get_json()
        telegram_process_message_service = TelegramProcessMessageService(
            callback_data_dao=CallbackDataDAO(),
        )
        telegram_process_message_service.execute(telegram_request=body)

        return '!'
