import settings
from telegram.ext import Updater


class TelegramRegisterWebhookService:

    def execute(self, telegram_webhook_path: str):
        telegram_webhook_url = '{}{}'.format(
            settings.TELEGRAM_WEBHOOK_BASE_URL, telegram_webhook_path
        )
        updater = Updater(token=settings.TELEGRAM_TOKEN)
        bot = updater.bot
        bot.delete_webhook()
        bot.set_webhook(url=telegram_webhook_url)
