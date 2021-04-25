from abc import ABC, abstractmethod
from typing import List, Optional

from domain.constants import Language
from domain.entities import PhraseToStudy, PhraseUsagesInDifferentLanguages


class IPhraseUsagesInDifferentLanguagesService(ABC):

    @abstractmethod
    def search(
        self,
        phrase: str,
        languages: List[Language],
        limit: int,
    ) -> PhraseUsagesInDifferentLanguages:
        pass


class ILanguageService(ABC):

    @abstractmethod
    def get_language(self, text: str) -> Language:
        pass


class IPhraseDAO(ABC):

    @abstractmethod
    def save_phrase(
        self,
        chat_id: str,
        source_phrase: str,
        target_phrase: str,
    ) -> None:
        pass

    @abstractmethod
    def get_phrase(self, chat_id: str) -> Optional[PhraseToStudy]:
        pass


class ICallbackDataDAO(ABC):

    @abstractmethod
    def save_data(self, data: dict) -> str:
        pass

    @abstractmethod
    def load_data(self, key: str) -> Optional[dict]:
        pass


class ILearnPhrasesDAO(ABC):

    @abstractmethod
    def save_translate(self, chat_id: str, translate: str) -> None:
        pass

    @abstractmethod
    def get_translate(self, chat_id: str) -> str:
        pass
