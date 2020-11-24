from typing import List

from domain.interfaces import (
    ILanguageService,
    IPhraseUsagesInDifferentLanguagesService
)
from domain.skills.phrase_search_skill import PhraseSearchSkill
from millet import Skill


def create_skill_classifier(
    language_service: ILanguageService,
    phrase_usages_in_different_languages_service: IPhraseUsagesInDifferentLanguagesService,
):

    def skill_classifier(message: str) -> List[Skill]:
        return [
            PhraseSearchSkill(
                language_service=language_service,
                phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
            )
        ]

    return skill_classifier
