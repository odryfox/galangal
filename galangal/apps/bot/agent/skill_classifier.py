from typing import List, Union

import bot.constants
from account.daos import AccountDAO
from bot.agent.skills import AddPhraseToStudySkill, SearchPhraseContextsSkill
from bot.agent.skills.greeting_skill import GreetingSkill
from bot.markdown import Action
from millet import BaseSkill, BaseSkillClassifier


class SkillClassifier(BaseSkillClassifier):

    GREETING_SKILL_KEY = 'GreetingSkill'
    ADD_PHRASE_TO_STUDY_SKILL_KEY = 'AddPhraseToStudySkill'
    SEARCH_PHRASE_CONTEXTS_SKILL_KEY = 'SearchPhraseContextsSkill'

    @property
    def skills_map(self) -> dict[str, BaseSkill]:
        return {
            self.GREETING_SKILL_KEY: GreetingSkill(),
            self.ADD_PHRASE_TO_STUDY_SKILL_KEY: AddPhraseToStudySkill(),
            self.SEARCH_PHRASE_CONTEXTS_SKILL_KEY: SearchPhraseContextsSkill(),
        }

    def classify(self, message: Union[str, dict], user_id: str) -> List[str]:
        skills = []

        is_account_exists = AccountDAO().is_account_exists(
            chat_id=user_id,
        )
        if not is_account_exists:
            skills.append(self.GREETING_SKILL_KEY)
            return skills

        if isinstance(message, Action):
            if message.action_type == bot.constants.ActionType.GREETING:
                skills.append(self.GREETING_SKILL_KEY)
            elif message.action_type == bot.constants.ActionType.ADD_PHRASE_TO_STUDY:
                skills.append(self.ADD_PHRASE_TO_STUDY_SKILL_KEY)
        elif isinstance(message, str):
            skills.append(self.SEARCH_PHRASE_CONTEXTS_SKILL_KEY)

        return skills
