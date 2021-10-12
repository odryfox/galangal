from telegram.ext import Updater


class TelegramRegisterWebhookService:

    def __init__(self, token: str):
        updater = Updater(token=token)
        self.bot = updater.bot

    def execute(self, url: str):
        self.bot.delete_webhook()
        self.bot.set_webhook(url=url)
