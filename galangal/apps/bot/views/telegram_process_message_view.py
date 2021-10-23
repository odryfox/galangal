from bot.messengers.telegram import create_telegram_process_message_service
from flask import request
from flask.views import MethodView


class TelegramProcessMessageView(MethodView):

    def post(self):

        body = request.get_json()
        telegram_process_message_service = create_telegram_process_message_service()
        telegram_process_message_service.execute(telegram_request=body)

        return '!'
