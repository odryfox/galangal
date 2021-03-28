from typing import List

from domain.agent.skills.add_phrase_to_study_skill import AddPhraseToStudySkill
from domain.agent.skills.greeting_skill import GreetingSkill
from domain.agent.skills.learn_phrases_skill import LearnPhrasesSkill
from domain.agent.skills.phrase_search_skill import PhraseSearchSkill
from domain.entities import (
    AddPhraseToStudySignal,
    GreetingSignal,
    LearnPhrasesSignal,
    UserRequest
)
from domain.interfaces import IPhraseDAO
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase
from millet import Agent, Skill
from millet.agent import BaseSkillClassifier


class SkillClassifier(BaseSkillClassifier):

    def __init__(
        self,
        search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
        save_phrase_to_study_usecase: SavePhraseToStudyUsecase,
        phrase_dao: IPhraseDAO,
    ):
        self.search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase
        self.save_phrase_to_study_usecase = save_phrase_to_study_usecase
        self.phrase_dao = phrase_dao

    def classify(self, message: UserRequest) -> List[Skill]:
        skills = []

        if isinstance(message.signal, AddPhraseToStudySignal):
            skill = AddPhraseToStudySkill(
                save_phrase_to_study_usecase=self.save_phrase_to_study_usecase,
            )
            skills.append(skill)
        elif isinstance(message.signal, GreetingSignal):
            skill = GreetingSkill()
            skills.append(skill)
        elif isinstance(message.signal, LearnPhrasesSignal):
            skill = LearnPhrasesSkill(phrase_dao=self.phrase_dao)
            skills.append(skill)
        elif message.message is not None:
            skill = PhraseSearchSkill(
                search_phrase_usages_in_different_languages_usecase=self.search_phrase_usages_in_different_languages_usecase,
            )
            skills.append(skill)

        return skills


def create_agent(
    search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
    save_phrase_to_study_usecase: SavePhraseToStudyUsecase,
    phrase_dao: IPhraseDAO,
) -> Agent:
    skill_classifier = SkillClassifier(
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        phrase_dao=phrase_dao,
    )
    agent = Agent(skill_classifier=skill_classifier)

    return agent
