from typing import Any, List, Tuple

from domain.constants import Language
from domain.entities import PhraseToStudy
from domain.interfaces import PhraseUsagesInDifferentLanguages
from infrastructure.bot.interfaces import IBot, UserRequest
from millet import Agent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater


class TelegramBot(IBot):

    def __init__(self, token: str, agent: Agent):
        self._token = token
        super().__init__(agent)

    def register_webhook(self, url: str) -> None:
        updater = Updater(token=self._token)
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=url)

    def _parse_request(self, request: dict) -> Tuple[UserRequest, str]:
        try:
            chat_id = request['message']['chat']['id']
            message = request['message']['text']
            signal = None
            data = {}
        except KeyError:
            chat_id = request['callback_query']['from']['id']
            message = None
            signal = 'add_word'
            data = request['callback_query']['data']

        user_request = UserRequest(
            message=message,
            signal=signal,
            data=data,
        )

        return user_request, chat_id

    def _send_response(self, response: Any, chat_id: str):
        if isinstance(response, str):
            self._send_message(message=response, chat_id=chat_id)
        elif isinstance(response, tuple):
            self._send_phrase_usages_in_different_languages(
                phrase_usages_in_different_languages=response[0],
                phrases_to_study=response[1],
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
        phrases_to_study: List[PhraseToStudy],
        chat_id: str,
    ) -> None:

        response = self._build_message_for_phrase_usages_in_different_languages(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=list(phrase_usages_in_different_languages[0].keys()),
        )
        keyboard = self._build_keyboard(
            phrases_to_study=phrases_to_study,
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
        phrases_to_study: List[PhraseToStudy],
    ) -> InlineKeyboardMarkup:

        buttons = []
        for phrase_to_study in phrases_to_study:
            text = '{} - {}'.format(phrase_to_study.source_phrase, phrase_to_study.target_phrase)

            button = InlineKeyboardButton(text='➕ {}'.format(text), callback_data=phrase_to_study.source_phrase)
            buttons.append(button)

        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        return keyboard
