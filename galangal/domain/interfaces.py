from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

from domain.constants import Language


@dataclass
class PhraseUsage:
    text: str
    phrase: str


PhraseUsageInDifferentLanguages = Dict[Language, PhraseUsage]
PhraseUsagesInDifferentLanguages = List[PhraseUsageInDifferentLanguages]


class IPhraseUsagesInDifferentLanguagesService(ABC):

    @abstractmethod
    def search(
        self,
        phrase: str,
        source_language: Language,
        target_languages: List[Language],
        limit: int,
    ) -> PhraseUsagesInDifferentLanguages:
        pass


class IBotService(ABC):

    def __init__(self, token: str) -> None:
        self._token = token

    @abstractmethod
    def register_webhook(self, url: str) -> None:
        pass

    @abstractmethod
    def send_message(self, chat_id: str, message: str) -> None:
        pass

    @abstractmethod
    def send_phrase_usages_in_different_languages(
        self,
        chat_id: str,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
        languages: List[Language]
    ) -> None:
        pass


class ILanguageService:

    @abstractmethod
    def get_language(self, text: str) -> Language:
        pass
