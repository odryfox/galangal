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


class ILanguageService(ABC):

    @abstractmethod
    def get_language(self, text: str) -> Language:
        pass
