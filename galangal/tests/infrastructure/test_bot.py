from unittest import mock
from unittest.mock import Mock

from domain.constants import Language
from domain.entities import PhraseUsage
from infrastructure.bot.telegram import TelegramBot


class TestTelegramBot:

    def setup_method(self):
        self.token = 'telegram_token'
        self.bot = TelegramBot(token=self.token)

    @mock.patch('infrastructure.bot.telegram.Updater')
    def test_register_webhook(self, updater_mock):
        url = 'https://server.com/webhook'

        bot_mock = Mock()
        updater_mock.return_value = Mock(bot=bot_mock)

        self.bot.register_webhook(url=url)

        bot_mock.delete_webhook()
        bot_mock.set_webhook.assert_called_once_with(url=url)

    @mock.patch('infrastructure.bot.telegram.Updater')
    def test_send_message(self, updater_mock):
        chat_id = 'terminator_chat_id'
        message = 'I will be back'

        bot_mock = Mock()
        updater_mock.return_value = Mock(bot=bot_mock)

        self.bot._send_message(
            chat_id=chat_id,
            message=message,
        )

        updater_mock.assert_called_once_with(token=self.token)
        bot_mock.send_message.assert_called_once_with(
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
    @mock.patch('infrastructure.bot.telegram.Updater')
    def test_send_phrase_usages_in_different_languages(
        self,
        updater_mock,
        build_keyboard_mock,
        build_message_for_phrase_usages_in_different_languages_mock,
    ):
        chat_id = 'terminator_chat_id'
        message = 'message'

        build_message_for_phrase_usages_in_different_languages_mock.return_value = message

        keyboard = mock.Mock()
        build_keyboard_mock.return_value = keyboard

        bot_mock = Mock()
        updater_mock.return_value = Mock(bot=bot_mock)

        phrase_usages_in_different_languages = [{Language.RU: mock.Mock(), Language.EN: mock.Mock()}]
        languages = [Language.RU, Language.EN]

        self.bot._send_phrase_usages_in_different_languages(
            chat_id=chat_id,
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
        )

        build_message_for_phrase_usages_in_different_languages_mock.assert_called_once_with(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=languages,
        )
        build_keyboard_mock.assert_called_once_with(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            languages=languages,
        )
        updater_mock.assert_called_once_with(token=self.token)
        bot_mock.send_message.assert_called_once_with(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=keyboard,
        )
