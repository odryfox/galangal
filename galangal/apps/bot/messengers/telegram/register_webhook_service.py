import bot.constants
import settings
from telegram.ext import Updater


class TelegramRegisterWebhookService:

    def execute(self):
        telegram_webhook_url = '{}{}'.format(
            settings.TELEGRAM_WEBHOOK_BASE_URL,
            bot.constants.TELEGRAM_WEBHOOK_PATH,
        )
        updater = Updater(token=settings.TELEGRAM_TOKEN)
        telegram_bot = updater.bot
        telegram_bot.delete_webhook()
        telegram_bot.set_webhook(url=telegram_webhook_url)
