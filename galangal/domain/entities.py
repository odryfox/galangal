from dataclasses import dataclass
from typing import Dict, List

from domain.constants import Language


@dataclass
class PhraseUsage:
    text: str
    phrase: str


PhraseUsageInDifferentLanguages = Dict[Language, PhraseUsage]
PhraseUsagesInDifferentLanguages = List[PhraseUsageInDifferentLanguages]
