from typing import List

from telegram.ext import Updater

from domain.constants import Language
from domain.interfaces import PhraseUsagesInDifferentLanguages
from domain.interfaces import IBotService


class TelegramService(IBotService):

    def register_webhook(self, url: str) -> None:
        updater = Updater(token=self._token)
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=url)

    def send_message(self, chat_id: str, message: str) -> None:
        updater = Updater(token=self._token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
        )

    def send_phrase_usages_in_different_languages(
        self,
        chat_id: str,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
        languages: List[Language]
    ) -> None:

        response = ''
        for phrase_usage_in_different_languages in phrase_usages_in_different_languages:
            for language in languages:
                phrase_usage = phrase_usage_in_different_languages[language]
                parts = phrase_usage.text.split(phrase_usage.phrase)
                target_text = "*{}*".format(phrase_usage.phrase).join(parts)
                response += target_text + '\n'

            response += '\n'

        updater = Updater(token=self._token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=response,
            parse_mode='Markdown',
        )
