from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from millet import Agent


@dataclass
class UserRequest:
    message: Optional[str]
    signal: Optional[str]
    data: dict


class IBot(ABC):

    def __init__(self, agent: Agent):
        self._agent = agent

    def execute(self, request: Any):
        user_request, chat_id = self._parse_request(request)
        responses = self._agent.query(message=user_request, user_id=chat_id)
        self._send_responses(responses=responses, chat_id=chat_id)

    @abstractmethod
    def _parse_request(self, request: Any) -> Tuple[UserRequest, str]:
        pass

    def _send_responses(self, responses: List[Any], chat_id: str):
        for response in responses:
            self._send_response(response, chat_id)

    @abstractmethod
    def _send_response(self, response: Any, chat_id: str):
        pass
