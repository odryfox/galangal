from typing import List, Dict

from telegram.ext import Updater

from domain.constants import LanguageEnum
from domain.entities import UsageCollocation
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

    def send_usages_of_collocation(
        self,
        chat_id: str,
        usages_of_collocation: List[Dict[LanguageEnum, UsageCollocation]],
        languages: List[LanguageEnum]
    ) -> None:
        response = ''
        for usage_collocation in usages_of_collocation:
            for language in languages:
                collocation = usage_collocation[language]
                parts = collocation.sentence.split(
                    collocation.collocation_from_sentence)
                target_text = "*{}*".format(
                    collocation.collocation_from_sentence).join(parts)
                response += target_text + '\n'

            response += '\n'

        updater = Updater(token=self.token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=response,
            parse_mode='Markdown',
        )
