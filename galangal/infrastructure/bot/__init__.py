from typing import List

from domain.usecases.phrase_to_study_usecases import (
    GetPhraseToStudyFromSearchUsecase
)
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot.interfaces import AddPhraseToStudySignal, UserRequest
from infrastructure.bot.skills import AddPhraseToStudySkill, PhraseSearchSkill
from millet import Agent, Skill


def _create_skill_classifier(
    search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
    get_phrases_to_study_from_search_usecase: GetPhraseToStudyFromSearchUsecase,
):

    def skill_classifier(message: UserRequest) -> List[Skill]:
        skills = []

        if isinstance(message.signal, AddPhraseToStudySignal):
            skill = AddPhraseToStudySkill()
            skills.append(skill)
        elif message.message is not None:
            skill = PhraseSearchSkill(
                search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
                get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            )
            skills.append(skill)

        return skills

    return skill_classifier


def create_agent(
    search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
    get_phrases_to_study_from_search_usecase: GetPhraseToStudyFromSearchUsecase,
):
    skill_classifier = _create_skill_classifier(
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
    )
    agent = Agent(skill_classifier=skill_classifier)

    return agent
