from typing import Any, Tuple

from infrastructure.bot.interfaces import IBot, UserRequest


class CLIBot(IBot):

    def _parse_request(self, request: str) -> Tuple[UserRequest, str]:

        if request[0] == '/':
            parts = request.split()
            message = None
            signal = parts[0][1:]
            if len(parts) > 1:
                data = parts[1]
            else:
                data = {}
        else:
            message = request
            signal = None
            data = {}

        user_request = UserRequest(
            message=message,
            signal=signal,
            data=data,
        )

        return user_request, 'console'

    def _send_response(self, response: Any, chat_id: str):
        print(response)
