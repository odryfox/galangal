from typing import Union

from domain.entities import PhraseToStudy
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

            if len(parts) > 2 and parts[0][1:] == AddPhraseToStudySignal.key:
                message = None
                signal = AddPhraseToStudySignal()
                phrase_to_study = PhraseToStudy(
                    source_phrase=parts[1],
                    target_phrase=parts[2],
                )
            else:
                message = request
                signal = None
                phrase_to_study = None
        else:
            message = request
            signal = None
            phrase_to_study = None

        user_request = UserRequest(
            chat_id=self.CHAT_ID,
            message=message,
            signal=signal,
            phrase_to_study=phrase_to_study,
        )

        return user_request

    def _send_response(self, response: Union[str, UserResponse], chat_id: str):
        print(response)
