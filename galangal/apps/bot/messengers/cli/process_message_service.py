from typing import List, Optional, Union

import bot.constants
from bot.agent import create_agent
from bot.markdown import Action, MarkdownDocument


class CLIProcessMessageService:

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
        agent = create_agent()
        chat_id = 'console'
        if isinstance(message, Action):
            user_responses: List[Union[str, MarkdownDocument]] = agent.process_action(
                message=message,
                user_id=chat_id,
            )
        else:
            user_responses: List[Union[str, MarkdownDocument]] = agent.process_message(
                message=message,
                user_id=chat_id,
            )
        for user_response in user_responses:
            self._send_user_response(user_response)
