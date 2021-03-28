from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

from domain.constants import Language


@dataclass
class PhraseUsage:
    text: str
    phrase: str


PhraseUsageInDifferentLanguages = Dict[Language, PhraseUsage]
PhraseUsagesInDifferentLanguages = List[PhraseUsageInDifferentLanguages]


@dataclass
class PhraseToStudy:
    source_phrase: str
    target_phrase: str


class UserSignal(ABC):

    @property
    @abstractmethod
    def key(self) -> str:
        pass


class AddPhraseToStudySignal(UserSignal):
    key = 'AddPhraseToStudySignal'


class GreetingSignal(UserSignal):
    key = 'GreetingSignal'


class LearnPhrasesSignal(UserSignal):
    key = 'LearnPhrasesSignal'


@dataclass
class UserRequest:
    chat_id: str
    message: Optional[str]
    signal: Optional[UserSignal]
    phrase_to_study: Optional[PhraseToStudy]


@dataclass
class UserResponse(ABC):
    pass


@dataclass
class SearchPhrasesResponse(UserResponse):
    phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages
    phrases_to_study: List[PhraseToStudy]


@dataclass
class GreetingResponse(UserResponse):
    text: str
