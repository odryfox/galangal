from unittest import mock
from unittest.mock import Mock

from domain.constants import Language
from domain.entities import (
    AddPhraseToStudySignal,
    PhraseToStudy,
    PhraseUsage,
    SearchPhrasesResponse
)
from infrastructure.telegram.bot import TelegramBot


class TestTelegramBot:

    def setup_method(self):
        self.token = 'telegram_token'
        self.callback_data_dao = mock.Mock()

        with mock.patch('infrastructure.telegram.bot.Updater') as updater_mock:
            self.updater_bot = mock.Mock()
            updater_mock.return_value = mock.Mock(bot=self.updater_bot)
            self.bot = TelegramBot(
                token=self.token,
                agent=mock.Mock(),
                callback_data_dao=self.callback_data_dao,
            )

        self.chat_id = 100500

    def test_register_webhook(self):
        url = 'https://server.com/webhook'

        self.bot.register_webhook(url=url)

        self.updater_bot.delete_webhook()
        self.updater_bot.set_webhook.assert_called_once_with(url=url)

    def test_send_message(self):
        chat_id = 'terminator_chat_id'
        message = 'I will be back'

        self.bot._send_message(
            chat_id=chat_id,
            message=message,
        )

        self.updater_bot.send_message.assert_called_once_with(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
        )

    def test_build_message_for_phrase_usages_in_different_languages__empty_message(self):
        message = self.bot._build_message_for_phrase_usages_in_different_languages(
            phrase_usages_in_different_languages=[],
            languages=[],
        )

        assert message == ''

    def test_build_message_for_phrase_usages_in_different_languages(self):
        phrase_usages_in_different_languages = [
            {
                Language.EN: PhraseUsage(
                    text="If anyone should phone, say I will be back at one o'clock.",
                    phrase='I will be back',
                ),
                Language.RU: PhraseUsage(
                    text='Если кто-нибудь позвонит, скажи, что я вернусь в час.',
                    phrase='я вернусь',
                ),
            },
            {
                Language.EN: PhraseUsage(
                    text='I will be back by 5, but just...',
                    phrase='I will be back',
                ),
                Language.RU: PhraseUsage(
                    text='Я вернусь к пяти, но если...',
                    phrase='Я вернусь',
                ),
            },
        ]

        message = self.bot._build_message_for_phrase_usages_in_different_languages(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=[Language.EN, Language.RU],
        )

        assert message == """If anyone should phone, say *I will be back* at one o'clock.
Если кто-нибудь позвонит, скажи, что *я вернусь* в час.

*I will be back* by 5, but just...
*Я вернусь* к пяти, но если...

"""

    @mock.patch.object(TelegramBot, '_build_message_for_phrase_usages_in_different_languages')
    @mock.patch.object(TelegramBot, '_build_keyboard')
    def test_send_phrase_usages_in_different_languages(
        self,
        build_keyboard_mock,
        build_message_for_phrase_usages_in_different_languages_mock,
    ):
        chat_id = 'terminator_chat_id'
        message = 'message'

        build_message_for_phrase_usages_in_different_languages_mock.return_value = message

        keyboard = mock.Mock()
        build_keyboard_mock.return_value = keyboard

        bot_mock = Mock()

        phrase_usages_in_different_languages = [{Language.RU: mock.Mock(), Language.EN: mock.Mock()}]
        phrases_to_study = mock.Mock()
        languages = [Language.RU, Language.EN]

        self.bot._send_phrase_usages_in_different_languages(
            chat_id=chat_id,
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            phrases_to_study=phrases_to_study,
        )

        build_message_for_phrase_usages_in_different_languages_mock.assert_called_once_with(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=languages,
        )
        build_keyboard_mock.assert_called_once_with(
            phrases_to_study=phrases_to_study,
        )
        self.updater_bot.send_message.assert_called_once_with(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=keyboard,
        )

    def test_build_keyboard__phrases(self):
        phrases_to_study = [
            PhraseToStudy(
                source_phrase='source_phrase',
                target_phrase='target_phrase',
            )
        ]

        self.callback_data_dao.save_data.return_value = 'key'

        callback_data = {
            'signal': AddPhraseToStudySignal.key,
            'phrase_to_study': {
                'source_phrase': 'source_phrase',
                'target_phrase': 'target_phrase',
            }
        }

        keyboard = self.bot._build_keyboard(phrases_to_study=phrases_to_study)

        self.callback_data_dao.save_data.assert_called_once_with(
            data=callback_data
        )

        assert len(keyboard.inline_keyboard) == 1
        line = keyboard.inline_keyboard[0]

        assert len(line) == 1
        button = line[0]

        assert button.text == '➕ source_phrase - target_phrase'
        assert button.callback_data == 'key'

    def test_build_keyboard__empty_phrases(self):
        phrases_to_study = []

        keyboard = self.bot._build_keyboard(phrases_to_study=phrases_to_study)

        assert keyboard.inline_keyboard == []

    def test_parse_request__without_signal(self):
        request = {
            'message': {
                'chat': {'id': self.chat_id},
                'text': 'I will be back'
            }
        }

        user_request = self.bot._parse_user_request(request)

        assert user_request.chat_id == str(self.chat_id)
        assert user_request.message == 'I will be back'
        assert user_request.signal is None
        assert user_request.phrase_to_study is None

    def test_parse_request__with_signal(self):
        request = {
            'callback_query': {
                'from': {'id': self.chat_id},
                'data': 'key',
            }
        }

        self.callback_data_dao.load_data.return_value = {
            'signal': AddPhraseToStudySignal.key,
            'phrase_to_study': {'source_phrase': 'data', 'target_phrase': 'hata'},
        }

        user_request = self.bot._parse_user_request(request)

        self.callback_data_dao.load_data.assert_called_once_with(key='key')

        assert user_request.chat_id == str(self.chat_id)
        assert user_request.message is None
        assert isinstance(user_request.signal, AddPhraseToStudySignal)
        assert user_request.phrase_to_study.source_phrase == 'data'
        assert user_request.phrase_to_study.target_phrase == 'hata'

    @mock.patch.object(TelegramBot, '_send_message')
    @mock.patch.object(TelegramBot, '_send_phrase_usages_in_different_languages')
    def test_send_response__str_response(self, send_phrase_usages_in_different_languages_mock, send_message_mock):
        user_response = 'user_response'

        self.bot._send_user_response(user_response=user_response, chat_id=str(self.chat_id))

        send_message_mock.assert_called_once_with(
            message=user_response, chat_id=str(self.chat_id)
        )
        send_phrase_usages_in_different_languages_mock.assert_not_called()

    @mock.patch.object(TelegramBot, '_send_message')
    @mock.patch.object(TelegramBot, '_send_phrase_usages_in_different_languages')
    def test_send_response__search_phrases_response(self, send_phrase_usages_in_different_languages_mock, send_message_mock):
        user_response = SearchPhrasesResponse(
            phrase_usages_in_different_languages=mock.Mock(),
            phrases_to_study=mock.Mock(),
        )

        self.bot._send_user_response(user_response=user_response, chat_id=str(self.chat_id))

        send_message_mock.assert_not_called()
        send_phrase_usages_in_different_languages_mock.assert_called_once_with(
            phrase_usages_in_different_languages=user_response.phrase_usages_in_different_languages,
            phrases_to_study=user_response.phrases_to_study,
            chat_id=str(self.chat_id),
        )

    @mock.patch.object(TelegramBot, '_send_message')
    @mock.patch.object(TelegramBot, '_send_phrase_usages_in_different_languages')
    def test_send_response__unknown_type_of_response(self, send_phrase_usages_in_different_languages_mock, send_message_mock):
        user_response = 100500

        self.bot._send_user_response(user_response=user_response, chat_id=str(self.chat_id))

        send_message_mock.assert_not_called()
        send_phrase_usages_in_different_languages_mock.assert_not_called()
