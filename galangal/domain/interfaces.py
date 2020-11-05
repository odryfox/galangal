from typing import List, Dict

from galangal.domain.constants import LanguageEnum
from galangal.domain.entities import UsageCollocation

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
