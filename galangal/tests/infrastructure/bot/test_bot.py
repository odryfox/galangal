from typing import Any, Tuple, Union
from unittest import mock

from infrastructure.bot.interfaces import IBot, UserRequest, UserResponse


class Bot(IBot):

    def _parse_request(self, request: Any) -> Tuple[UserRequest, str]:
        pass

    def _send_response(self, response: Union[str, UserResponse], chat_id: str) -> None:
        pass


class TestBot:

    def setup_method(self):
        self.agent_mock = mock.Mock()
        self.bot = Bot(agent=self.agent_mock)

    @mock.patch.object(Bot, '_send_response')
    def test_send_responses(self, send_response_mock):

        responses = ['1', '2', '3']
        chat_id = '100500'

        self.bot._send_responses(responses=responses, chat_id=chat_id)

        expected_calls = [
            mock.call('1', chat_id),
            mock.call('2', chat_id),
            mock.call('3', chat_id),
        ]

        assert send_response_mock.mock_calls == expected_calls

    @mock.patch.object(Bot, '_parse_request')
    @mock.patch.object(Bot, '_send_responses')
    def test_execute(self, send_responses_mock, parse_request_mock):
        request = mock.Mock()
        user_request = mock.Mock()
        chat_id = mock.Mock()

        parse_request_mock.return_value = tuple([user_request, chat_id])

        responses = mock.Mock()
        self.agent_mock.query.return_value = responses

        self.bot.execute(request=request)

        parse_request_mock.assert_called_once_with(request)
        self.agent_mock.query.assert_called_once_with(
            message=user_request, user_id=chat_id
        )
        send_responses_mock.assert_called_once_with(
            responses=responses, chat_id=chat_id
        )
