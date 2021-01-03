from typing import Tuple, Union

from infrastructure.bot.interfaces import (
    AddPhraseToStudySignal,
    IBot,
    UserRequest,
    UserResponse
)


class CLIBot(IBot):

    def _parse_request(self, request: str) -> Tuple[UserRequest, str]:

        if request[0] == '/':
            parts = request.split()
            message = None

            signal = parts[0][1:]
            if signal == 'add_phrase_to_study':
                signal = AddPhraseToStudySignal()
            else:
                signal = None

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

    def _send_response(self, response: Union[str, UserResponse], chat_id: str):
        print(response)
