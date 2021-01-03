from unittest import mock

from infrastructure.bot import AddPhraseToStudySignal
from infrastructure.bot.cli import CLIBot


class TestCLIBot:

    def setup_method(self):
        self.bot = CLIBot(agent=mock.Mock())

    def test_parse_request__without_signal(self):
        request = 'I will be back'

        user_request, chat_id = self.bot._parse_request(request=request)

        assert chat_id, 'console'
        assert user_request.message == 'I will be back'
        assert user_request.signal is None
        assert user_request.data == {}

    def test_parse_request__with_signal(self):
        request = '/add_phrase_to_study data'

        user_request, chat_id = self.bot._parse_request(request=request)

        assert chat_id, 'console'
        assert user_request.message is None
        assert isinstance(user_request.signal, AddPhraseToStudySignal)
        assert user_request.data == 'data'

    def test_parse_request__unknown_signal(self):
        request = '/unknown_signal data'

        user_request, chat_id = self.bot._parse_request(request=request)

        assert chat_id, 'console'
        assert user_request.message is None
        assert user_request.signal is None
        assert user_request.data == 'data'

    def test_parse_request__signal_without_data(self):
        request = '/add_phrase_to_study'

        user_request, chat_id = self.bot._parse_request(request=request)

        assert chat_id, 'console'
        assert user_request.message is None
        assert isinstance(user_request.signal, AddPhraseToStudySignal)
        assert user_request.data == {}

    @mock.patch('builtins.print')
    def test_send_response(self, print_mock):
        response = 'response'
        chat_id = 'console'

        self.bot._send_response(response=response, chat_id=chat_id)

        print_mock.assert_called_once_with(response)
