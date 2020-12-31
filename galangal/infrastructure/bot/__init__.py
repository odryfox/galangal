from typing import List

from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot.skills import PhraseSearchSkill
from millet import Agent, Skill


def _create_skill_classifier(
    search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
):

    def skill_classifier(message: str) -> List[Skill]:
        return [
            PhraseSearchSkill(
                search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase
            )
        ]

    return skill_classifier


def create_agent(
    search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
):
    skill_classifier = _create_skill_classifier(
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
    )
    agent = Agent(skill_classifier=skill_classifier)

    return agent
