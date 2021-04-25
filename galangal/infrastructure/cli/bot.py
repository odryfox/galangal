from typing import Union

from domain.entities import (
    AddPhraseToStudySignal,
    LearnPhrasesSignal,
    PhraseToStudy,
    UserRequest,
    UserResponse
)
from millet import Agent


class CLIBot:

    CHAT_ID = 'console'

    def __init__(self, agent: Agent):
        self.agent = agent

    def process_request(self, request: str) -> None:
        user_request = self._parse_request(request)
        user_responses = self.agent.query(
            message=user_request,
            user_id=user_request.chat_id,
        )
        for user_response in user_responses:
            self._send_user_response(user_response)

    def _parse_request(self, request) -> UserRequest:
        if request[0] == '/':
            parts = request.split()

            if len(parts) > 2 and parts[0][1:] == AddPhraseToStudySignal.key:
                message = None
                signal = AddPhraseToStudySignal()
                phrase_to_study = PhraseToStudy(
                    source_phrase=parts[1],
                    target_phrase=parts[2],
                )
            elif parts[0][1:] == LearnPhrasesSignal.key:
                message = None
                signal = LearnPhrasesSignal()
                phrase_to_study = None
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

    def _send_user_response(self, user_response: Union[str, UserResponse]):
        print(user_response)
