from typing import List, Tuple, Union

from domain.constants import Language
from domain.entities import PhraseToStudy
from domain.interfaces import PhraseUsagesInDifferentLanguages
from infrastructure.bot.interfaces import (
    AddPhraseToStudySignal,
    IBot,
    ICallbackDataDAO,
    SearchPhrasesResponse,
    UserRequest,
    UserResponse
)
from millet import Agent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater


class TelegramBot(IBot):

    def __init__(
        self,
        token: str,
        agent: Agent,
        callback_data_dao: ICallbackDataDAO,
    ):
        self._token = token
        self._callback_data_dao = callback_data_dao
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
            signal = None
            data = {}
            callback_key = request['callback_query']['data']
            callback_data = self._callback_data_dao.load_data(key=callback_key)
            if callback_data and callback_data['signal'] == AddPhraseToStudySignal.key:
                signal = AddPhraseToStudySignal()
                data = callback_data['data']

        user_request = UserRequest(
            message=message,
            signal=signal,
            data=data,
        )

        return user_request, chat_id

    def _send_response(self, response: Union[str, UserResponse], chat_id: str):
        if isinstance(response, str):
            self._send_message(message=response, chat_id=chat_id)
        elif isinstance(response, SearchPhrasesResponse):
            self._send_phrase_usages_in_different_languages(
                phrase_usages_in_different_languages=response.phrase_usages_in_different_languages,
                phrases_to_study=response.phrases_to_study,
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

            callback_data = {
                'signal': AddPhraseToStudySignal.key,
                'data': {
                    'source_phrase': phrase_to_study.source_phrase,
                    'target_phrase': phrase_to_study.target_phrase,
                }
            }

            callback_key = self._callback_data_dao.save_data(data=callback_data)

            button = InlineKeyboardButton(text='➕ {}'.format(text), callback_data=callback_key)
            buttons.append(button)

        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        return keyboard
