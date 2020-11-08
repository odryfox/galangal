from typing import List, Dict

from domain.constants import LanguageEnum
from domain.entities import UsageCollocation

from abc import ABC, abstractmethod


class IUsageCollocationsService(ABC):

    @abstractmethod
    def search(
        self,
        collocation: str,
        source_language: LanguageEnum,
        target_language: LanguageEnum,
        limit: int,
    ) -> List[Dict[LanguageEnum, UsageCollocation]]:
        pass


class ITelegramService(ABC):

    def __init__(self, token: str) -> None:
        self.token = token

    @abstractmethod
    def register_webhook(self, url: str) -> None:
        pass

    @abstractmethod
    def send_message(self, chat_id: str, message: str) -> None:
        pass

    @abstractmethod
    def send_usages_of_collocation(
        self,
        chat_id: str,
        usages_of_collocation: List[Dict[LanguageEnum, UsageCollocation]],
        languages: List[LanguageEnum]
    ) -> None:
        pass
