from typing import List, Optional, Tuple, Union

from bot.daos import CallbackDataDAO
from bot.markdown import (
    Action,
    MarkdownActionComponent,
    MarkdownChoiceComponent,
    MarkdownDocument,
    MarkdownImportantTextComponent,
    MarkdownTextComponent
)
from millet import Agent
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from telegram.ext import Updater


class TelegramProcessMessageService:

    def __init__(
        self,
        token: str,
        agent: Agent,
        callback_data_dao: CallbackDataDAO,
    ) -> None:
        updater = Updater(token=token)
        self.bot = updater.bot

        self.agent = agent
        self.callback_data_dao = callback_data_dao

    def _parse_user_request(
        self,
        telegram_request: dict,
    ) -> Tuple[Optional[Union[str, Action]], Optional[str]]:
        try:
            chat_id = telegram_request['message']['chat']['id']
            message = telegram_request['message']['text']
        except KeyError:
            try:
                chat_id = telegram_request['callback_query']['from']['id']
                callback_key = telegram_request['callback_query']['data']
                callback_data = self.callback_data_dao.load_data(
                    key=callback_key
                )
                if 'action' in callback_data:
                    message = Action(
                        action_type=callback_data['action']['action_type'],
                        params=callback_data['action']['params'],
                    )
                else:
                    message = None
            except KeyError:
                message = None
                chat_id = None

        return message, chat_id

    def _send_message(
        self,
        message: str,
        chat_id: str,
        keyboard: ReplyKeyboardMarkup = None,
    ) -> None:
        self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=keyboard,
        )

    def _build_menu(
        self,
        choices_components: List[MarkdownChoiceComponent],
    ) -> ReplyKeyboardMarkup:
        buttons = [
            [
                KeyboardButton(text=choice_component.text)
                for choice_component in choices_components
            ]
        ]
        return ReplyKeyboardMarkup(keyboard=buttons)

    def _build_action_buttons(
        self,
        actions_components: List[MarkdownActionComponent],
    ) -> InlineKeyboardMarkup:

        buttons = []
        for action_component in actions_components:
            data = {
                'action': {
                    'action_type': action_component.action.action_type,
                    'params': action_component.action.params,
                }
            }
            callback_key = self.callback_data_dao.save_data(
                data=data
            )
            button = InlineKeyboardButton(
                text=action_component.text,
                callback_data=callback_key,
            )
            buttons.append(button)

        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        return keyboard

    def _send_user_response(
        self,
        user_response: MarkdownDocument,
        chat_id: str,
    ) -> None:
        message = ''
        actions_components = []
        choices_components = []

        for component in user_response.components:
            if isinstance(component, str):
                message += component
            if isinstance(component, MarkdownTextComponent):
                message += component.text
            elif isinstance(component, MarkdownImportantTextComponent):
                message += '*{}*'.format(component.text)
            elif isinstance(component, MarkdownActionComponent):
                actions_components.append(component)
            elif isinstance(component, MarkdownChoiceComponent):
                choices_components.append(component)

        if choices_components:
            keyboard = self._build_menu(choices_components=choices_components)
        elif actions_components:
            keyboard = self._build_action_buttons(actions_components=actions_components)
        else:
            keyboard = None

        self._send_message(
            message=message, chat_id=chat_id, keyboard=keyboard
        )

    def execute(self, telegram_request: dict) -> None:
        message, chat_id = self._parse_user_request(telegram_request)

        if not message or not chat_id:
            return

        user_responses: List[MarkdownDocument] = self.agent.query(
            message=message,
            user_id=chat_id,
        )
        for user_response in user_responses:
            self._send_user_response(user_response, chat_id)