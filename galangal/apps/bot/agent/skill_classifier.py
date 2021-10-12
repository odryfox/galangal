from typing import List, Union

import bot.constants
from bot.agent.skills import AddPhraseToStudySkill, SearchPhraseContextsSkill
from bot.agent.skills.greeting_skill import GreetingSkill
from bot.markdown import Action
from millet import BaseSkill, BaseSkillClassifier
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase
from vocabulary_trainer.use_cases import (
    AddPhraseToStudyUseCase,
    SuggestPhrasesToStudyUseCase
)


class SkillClassifier(BaseSkillClassifier):

    GREETING_SKILL_KEY = 'GreetingSkill'
    ADD_PHRASE_TO_STUDY_SKILL_KEY = 'AddPhraseToStudySkill'
    SEARCH_PHRASE_CONTEXTS_SKILL_KEY = 'SearchPhraseContextsSkill'

    def __init__(
        self,
        add_phrase_to_study_use_case: AddPhraseToStudyUseCase,
        search_phrase_contexts_use_case: SearchPhraseContextsUseCase,
        suggest_phrases_to_study_use_case: SuggestPhrasesToStudyUseCase,
    ) -> None:
        self.add_phrase_to_study_use_case = add_phrase_to_study_use_case
        self.search_phrase_contexts_use_case = search_phrase_contexts_use_case
        self.suggest_phrases_to_study_use_case = suggest_phrases_to_study_use_case

    @property
    def skills_map(self) -> dict[str, BaseSkill]:
        return {
            self.GREETING_SKILL_KEY: GreetingSkill(),
            self.ADD_PHRASE_TO_STUDY_SKILL_KEY: AddPhraseToStudySkill(
                add_phrase_to_study_use_case=self.add_phrase_to_study_use_case,
            ),
            self.SEARCH_PHRASE_CONTEXTS_SKILL_KEY: SearchPhraseContextsSkill(
                search_phrase_contexts_use_case=self.search_phrase_contexts_use_case,
                suggest_phrases_to_study_use_case=self.suggest_phrases_to_study_use_case,
            ),
        }

    def classify(self, message: Union[str, dict]) -> List[str]:
        skills = []

        if isinstance(message, Action):
            if message.action_type == bot.constants.ActionType.GREETING:
                skills.append(self.GREETING_SKILL_KEY)
            elif message.action_type == bot.constants.ActionType.ADD_PHRASE_TO_STUDY:
                skills.append(self.ADD_PHRASE_TO_STUDY_SKILL_KEY)
        elif isinstance(message, str):
            skills.append(self.SEARCH_PHRASE_CONTEXTS_SKILL_KEY)

        return skills
