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
from millet import Agent, BaseSkill
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

    @property
    def skills_map(self) -> dict[str, BaseSkill]:
        return {
            'AddPhraseToStudySkill': AddPhraseToStudySkill(
                save_phrase_to_study_usecase=self.save_phrase_to_study_usecase,
            ),
            'GreetingSkill': GreetingSkill(),
            'LearnPhrasesSkill': LearnPhrasesSkill(phrase_dao=self.phrase_dao),
            'PhraseSearchSkill': PhraseSearchSkill(
                search_phrase_usages_in_different_languages_usecase=self.search_phrase_usages_in_different_languages_usecase,
            ),
        }

    def classify(self, message: UserRequest) -> List[str]:
        skills = []

        if isinstance(message.signal, AddPhraseToStudySignal):
            skills.append('AddPhraseToStudySkill')
        elif isinstance(message.signal, GreetingSignal):
            skills.append('GreetingSkill')
        elif isinstance(message.signal, LearnPhrasesSignal):
            skills.append('LearnPhrasesSkill')
        elif message.message is not None:
            skills.append('PhraseSearchSkill')

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
