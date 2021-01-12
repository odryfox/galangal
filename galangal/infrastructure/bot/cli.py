from typing import Union

from infrastructure.bot.interfaces import (
    AddPhraseToStudySignal,
    IBot,
    UserRequest,
    UserResponse
)


class CLIBot(IBot):

    CHAT_ID = 'console'

    def _parse_request(self, request: str) -> UserRequest:

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
            chat_id=self.CHAT_ID,
            message=message,
            signal=signal,
            data=data,
        )

        return user_request

    def _send_response(self, response: Union[str, UserResponse], chat_id: str):
        print(response)
