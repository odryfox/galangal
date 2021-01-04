from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Union

from domain.entities import PhraseToStudy, PhraseUsagesInDifferentLanguages
from millet import Agent


class UserSignal(ABC):

    @property
    @abstractmethod
    def key(self) -> str:
        pass


class AddPhraseToStudySignal(UserSignal):

    key = 'AddPhraseToStudySignal'


@dataclass
class UserRequest:
    message: Optional[str]
    signal: Optional[UserSignal]
    data: dict


@dataclass
class UserResponse(ABC):
    pass


@dataclass
class SearchPhrasesResponse(UserResponse):
    phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages
    phrases_to_study: List[PhraseToStudy]


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

    def _send_responses(self, responses: List[Union[str, UserResponse]], chat_id: str):
        for response in responses:
            self._send_response(response, chat_id)

    @abstractmethod
    def _send_response(self, response: Union[str, UserResponse], chat_id: str) -> None:
        pass


class ICallbackDataDAO(ABC):

    @abstractmethod
    def save_data(self, data: dict) -> str:
        pass

    @abstractmethod
    def load_data(self, key: str) -> Optional[dict]:
        pass
