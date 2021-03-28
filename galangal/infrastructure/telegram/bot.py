from typing import List, Optional

from domain.constants import Language
from domain.entities import (
    AddPhraseToStudySignal,
    GreetingResponse,
    GreetingSignal,
    LearnPhrasesSignal,
    PhraseToStudy,
    PhraseUsagesInDifferentLanguages,
    SearchPhrasesResponse,
    UserRequest,
    UserResponse
)
from domain.interfaces import ICallbackDataDAO
from millet import Agent
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from telegram.ext import Updater


class TelegramBot:

    def __init__(
        self,
        token: str,
        agent: Agent,
        callback_data_dao: ICallbackDataDAO,
    ) -> None:
        self.token = token
        self.callback_data_dao = callback_data_dao
        self.agent = agent

        updater = Updater(token=self.token)
        self.bot = updater.bot

    def register_webhook(self, url: str) -> None:
        self.bot.delete_webhook()
        self.bot.set_webhook(url=url)

    def process_request(self, request):
        user_request = self._parse_user_request(request)
        if not user_request:
            return

        user_responses = self.agent.query(
            message=user_request,
            user_id=user_request.chat_id,
        )
        for user_response in user_responses:
            self._send_user_response(user_response, user_request.chat_id)

    def _parse_user_request(self, request) -> Optional[UserRequest]:
        try:
            chat_id = request['message']['chat']['id']
            message = request['message']['text']
            signal = None
            if message == '/start':
                message = None
                signal = GreetingSignal()
            elif message == 'Изучение слов':
                message = None
                signal = LearnPhrasesSignal()
            phrase_to_study = None
        except KeyError:
            try:
                chat_id = request['callback_query']['from']['id']
                message = None
                signal = None
                phrase_to_study = None
                callback_key = request['callback_query']['data']
                callback_data = self.callback_data_dao.load_data(key=callback_key)
                if callback_data and callback_data['signal'] == AddPhraseToStudySignal.key:
                    signal = AddPhraseToStudySignal()
                    phrase_to_study = PhraseToStudy(
                        source_phrase=callback_data['phrase_to_study']['source_phrase'],
                        target_phrase=callback_data['phrase_to_study']['target_phrase'],
                    )
            except KeyError:
                return

        user_request = UserRequest(
            chat_id=str(chat_id),
            message=message,
            signal=signal,
            phrase_to_study=phrase_to_study,
        )

        return user_request

    def _send_user_response(self, user_response: UserResponse, chat_id: str):
        if isinstance(user_response, str):
            self._send_message(message=user_response, chat_id=chat_id)
        elif isinstance(user_response, SearchPhrasesResponse):
            self._send_phrase_usages_in_different_languages(
                phrase_usages_in_different_languages=user_response.phrase_usages_in_different_languages,
                phrases_to_study=user_response.phrases_to_study,
                chat_id=chat_id,
            )
        elif isinstance(user_response, GreetingResponse):
            menu = self._build_menu()
            self._send_message_with_menu(message=user_response.text, chat_id=chat_id, menu=menu)

    def _send_message(self, message: str, chat_id: str) -> None:
        self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
        )

    def _send_message_with_menu(self, message: str, chat_id: str, menu: ReplyKeyboardMarkup) -> None:
        self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=menu,
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
        self.bot.send_message(
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
            text = '{} - {}'.format(phrase_to_study.source_phrase,
                                    phrase_to_study.target_phrase)

            callback_data = {
                'signal': AddPhraseToStudySignal.key,
                'phrase_to_study': {
                    'source_phrase': phrase_to_study.source_phrase,
                    'target_phrase': phrase_to_study.target_phrase,
                }
            }

            callback_key = self.callback_data_dao.save_data(data=callback_data)

            button = InlineKeyboardButton(
                text='➕ {}'.format(text),
                callback_data=callback_key,
            )
            buttons.append(button)

        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        return keyboard

    def _build_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [
                KeyboardButton(text='Изучение слов'),
            ],
        ]

        menu = ReplyKeyboardMarkup(
            keyboard=buttons,
        )
        return menu
