from bot.messengers.telegram import TelegramRegisterWebhookService
from flask.views import MethodView


class TelegramRegisterWebhookView(MethodView):
    def __init__(
        self,
        telegram_register_webhook_service: TelegramRegisterWebhookService,
        telegram_webhook_url: str,
    ) -> None:
        self.telegram_register_webhook_service = telegram_register_webhook_service
        self.telegram_webhook_url = telegram_webhook_url

        super().__init__()

    def get(self):
        self.telegram_register_webhook_service.execute(
            url=self.telegram_webhook_url,
        )
        return '!'
