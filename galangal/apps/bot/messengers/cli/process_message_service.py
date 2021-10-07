from typing import List, Optional, Union

import bot.constants
from bot.markdown import Action, MarkdownDocument
from millet import Agent


class CLIProcessMessageService:

    def __init__(
        self,
        agent: Agent,
    ) -> None:
        self.agent = agent

    def _send_user_response(
        self,
        user_response: MarkdownDocument,
    ) -> None:
        print(user_response)

    def _parse_user_request(
        self,
        request: Optional[str],
    ) -> Union[str, Action]:
        if request is None:
            message = Action(
                action_type=bot.constants.ActionType.GREETING,
                params={},
            )
        else:
            message = request
        return message

    def execute(self, request: Optional[str]) -> None:
        message = self._parse_user_request(request)
        user_responses: List[MarkdownDocument] = self.agent.query(
            message=message,
            user_id='console',
        )
        for user_response in user_responses:
            self._send_user_response(user_response)
