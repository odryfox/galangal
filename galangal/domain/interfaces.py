from abc import ABC, abstractmethod
from typing import List

from domain.constants import Language
from domain.entities import PhraseUsagesInDifferentLanguages


class IPhraseUsagesInDifferentLanguagesService(ABC):

    @abstractmethod
    def search(
        self,
        phrase: str,
        languages: List[Language],
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
