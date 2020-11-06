from telegram.ext import Updater

from domain.interfaces import ITelegramService


class TelegramService(ITelegramService):

    def register_webhook(self, url: str) -> None:
        updater = Updater(token=self.token)
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=url)

    def send_message(self, chat_id: str, message: str) -> None:
        updater = Updater(token=self.token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
        )
