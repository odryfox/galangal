from typing import List

from domain.constants import Language
from domain.interfaces import PhraseUsagesInDifferentLanguages
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater


class TelegramService:

    def __init__(self, token: str):
        self._token = token

    def register_webhook(self, url: str) -> None:
        updater = Updater(token=self._token)
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=url)

    def send_message(self, chat_id: str, message: str, keyboard=None) -> None:
        updater = Updater(token=self._token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=keyboard,
        )

    def _build_message_for_phrase_usages_in_different_languages(
        self,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
        languages: List[Language],
    ) -> str:

        message = ''

        for phrase_usage_in_different_languages in phrase_usages_in_different_languages:
            for language in languages:
                phrase_usage = phrase_usage_in_different_languages[language]
                parts = phrase_usage.text.split(phrase_usage.phrase)
                target_text = "*{}*".format(phrase_usage.phrase).join(parts)
                message += target_text + '\n'

            message += '\n'

        return message

    def _build_keyboard(
        self,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
        languages: List[Language],
    ) -> InlineKeyboardMarkup:

        phrases = []
        language = languages[1]
        for phrase_usage_in_different_languages in phrase_usages_in_different_languages:
            phrase_usage = phrase_usage_in_different_languages[language]
            phrase = phrase_usage.phrase
            if phrase not in phrases:
                phrases.append(phrase_usage.phrase)

        buttons = []
        for phrase in phrases:
            button = InlineKeyboardButton(text='➕ {}'.format(phrase), callback_data=phrase)
            buttons.append(button)

        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        return keyboard

    def send_phrase_usages_in_different_languages(
        self,
        chat_id: str,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
        languages: List[Language]
    ) -> None:

        response = self._build_message_for_phrase_usages_in_different_languages(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=list(phrase_usages_in_different_languages[0].keys()),
        )
        keyboard = self._build_keyboard(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=list(phrase_usages_in_different_languages[0].keys()),
        )
        self.send_message(
            chat_id=chat_id,
            message=response,
            keyboard=keyboard,
        )
