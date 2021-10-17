from bot.messengers.telegram import TelegramRegisterWebhookService
from flask.views import MethodView


class TelegramRegisterWebhookView(MethodView):
    def __init__(self, telegram_webhook_path: str) -> None:
        self.telegram_webhook_path = telegram_webhook_path

        super().__init__()

    def get(self):
        telegram_register_webhook_service = TelegramRegisterWebhookService()
        telegram_register_webhook_service.execute(
            telegram_webhook_path=self.telegram_webhook_path,
        )
        return '!'
