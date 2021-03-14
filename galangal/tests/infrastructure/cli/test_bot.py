from unittest import mock

from domain.entities import AddPhraseToStudySignal
from infrastructure.cli.bot import CLIBot


class TestCLIBot:

    def setup_method(self):
        self.bot = CLIBot(agent=mock.Mock())

    def test_parse_request__without_signal(self):
        request = 'I will be back'

        user_request = self.bot._parse_request(request=request)

        assert user_request.chat_id, self.bot.CHAT_ID
        assert user_request.message == 'I will be back'
        assert user_request.signal is None
        assert user_request.phrase_to_study == None

    def test_parse_request__with_signal(self):
        request = '/AddPhraseToStudySignal data hata'

        user_request = self.bot._parse_request(request=request)

        assert user_request.chat_id, self.bot.CHAT_ID
        assert user_request.message is None
        assert isinstance(user_request.signal, AddPhraseToStudySignal)
        assert user_request.phrase_to_study.source_phrase == 'data'
        assert user_request.phrase_to_study.target_phrase == 'hata'

    def test_parse_request__unknown_signal(self):
        request = '/unknown_signal data'

        user_request = self.bot._parse_request(request=request)

        assert user_request.chat_id, self.bot.CHAT_ID
        assert user_request.message == request
        assert user_request.signal is None
        assert user_request.phrase_to_study is None

    def test_parse_request__signal_without_data(self):
        request = '/AddPhraseToStudySignal'

        user_request = self.bot._parse_request(request=request)

        assert user_request.chat_id, self.bot.CHAT_ID
        assert user_request.message == request
        assert user_request.signal is None
        assert user_request.phrase_to_study is None

    @mock.patch('builtins.print')
    def test_send_response(self, print_mock):
        response = 'response'

        self.bot._send_user_response(user_response=response)

        print_mock.assert_called_once_with(response)
