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
from domain.interfaces import ILearnPhrasesDAO, IPhraseDAO
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase
from millet import Agent, BaseSkill
from millet.agent import BaseSkillClassifier
from millet.context import RedisContextManager
from redis import Redis


class SkillClassifier(BaseSkillClassifier):

    def __init__(
        self,
        search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
        save_phrase_to_study_usecase: SavePhraseToStudyUsecase,
        phrase_dao: IPhraseDAO,
        learn_phrases_dao: ILearnPhrasesDAO,
    ):
        self.search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase
        self.save_phrase_to_study_usecase = save_phrase_to_study_usecase
        self.phrase_dao = phrase_dao
        self.learn_phrases_dao = learn_phrases_dao

    @property
    def skills_map(self) -> dict[str, BaseSkill]:
        return {
            'AddPhraseToStudySkill': AddPhraseToStudySkill(
                save_phrase_to_study_usecase=self.save_phrase_to_study_usecase,
            ),
            'GreetingSkill': GreetingSkill(),
            'LearnPhrasesSkill': LearnPhrasesSkill(
                phrase_dao=self.phrase_dao,
                learn_phrases_dao=self.learn_phrases_dao
            ),
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
    learn_phrases_dao: ILearnPhrasesDAO,
    redis: Redis,
) -> Agent:

    skill_classifier = SkillClassifier(
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        phrase_dao=phrase_dao,
        learn_phrases_dao=learn_phrases_dao,
    )
    redis_context_manager = RedisContextManager(redis=redis)
    agent = Agent(
        skill_classifier=skill_classifier,
        context_manager=redis_context_manager,
    )

    return agent
