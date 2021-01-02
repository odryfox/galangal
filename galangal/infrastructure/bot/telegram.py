from typing import Any, List, Tuple

from domain.constants import Language
from domain.interfaces import PhraseUsagesInDifferentLanguages
from infrastructure.bot.interfaces import IBot, UserRequest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater


class TelegramBot(IBot):

    def __init__(self, token: str):
        self._token = token

    def register_webhook(self, url: str) -> None:
        updater = Updater(token=self._token)
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=url)

    def parse_request(self, body: dict) -> Tuple[UserRequest, str]:
        try:
            chat_id = body['message']['chat']['id']
            message = body['message']['text']
            signal = None
            data = {}
        except KeyError:
            chat_id = body['callback_query']['from']['id']
            message = None
            signal = 'add_word'
            data = body['callback_query']['data']

        user_request = UserRequest(
            message=message,
            signal=signal,
            data=data,
        )

        return user_request, chat_id

    def send_response(self, response: Any, chat_id: str):
        if isinstance(response, str):
            self._send_message(message=response, chat_id=chat_id)
        elif isinstance(response, list):
            self._send_phrase_usages_in_different_languages(
                phrase_usages_in_different_languages=response,
                chat_id=chat_id,
            )

    def _send_message(self, message: str, chat_id: str) -> None:
        updater = Updater(token=self._token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
        )

    def _send_phrase_usages_in_different_languages(
        self,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
        chat_id: str,
    ) -> None:

        response = self._build_message_for_phrase_usages_in_different_languages(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=list(phrase_usages_in_different_languages[0].keys()),
        )
        keyboard = self._build_keyboard(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=list(phrase_usages_in_different_languages[0].keys()),
        )
        updater = Updater(token=self._token)
        updater.bot.send_message(
            chat_id=chat_id,
            text=response,
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

        source_language = languages[0]
        target_language = languages[1]

        phrases = set()

        for phrase_usage_in_different_languages in phrase_usages_in_different_languages:
            phrase_usage_in_source_language = phrase_usage_in_different_languages[source_language].phrase.lower()
            phrase_usage_in_target_language = phrase_usage_in_different_languages[target_language].phrase.lower()
            phrases.add((phrase_usage_in_source_language, phrase_usage_in_target_language))

        buttons = []
        for phrase in phrases:
            phrase_usage_in_source_language = phrase[0]
            phrase_usage_in_target_language = phrase[1]

            text = '{} - {}'.format(phrase_usage_in_source_language, phrase_usage_in_target_language)

            button = InlineKeyboardButton(text='➕ {}'.format(text), callback_data=phrase_usage_in_source_language)
            buttons.append(button)

        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        return keyboard
