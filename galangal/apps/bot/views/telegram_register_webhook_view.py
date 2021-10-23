from bot.messengers.telegram import TelegramRegisterWebhookService
from flask.views import MethodView


class TelegramRegisterWebhookView(MethodView):

    def get(self):
        telegram_register_webhook_service = TelegramRegisterWebhookService()
        telegram_register_webhook_service.execute()
        return '!'
