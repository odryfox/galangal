from dataclasses import dataclass
from typing import Dict, List

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
