from bot.agent.skill_classifier import SkillClassifier
from millet import Agent
from millet.context import RedisContextManager
from redis import Redis
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase
from vocabulary_trainer.use_cases import (
    AddPhraseToStudyUseCase,
    SuggestPhrasesToStudyUseCase
)


def create_agent(
    add_phrase_to_study_use_case: AddPhraseToStudyUseCase,
    search_phrase_contexts_use_case: SearchPhraseContextsUseCase,
    suggest_phrases_to_study_use_case: SuggestPhrasesToStudyUseCase,
    redis: Redis,
) -> Agent:

    skill_classifier = SkillClassifier(
        add_phrase_to_study_use_case=add_phrase_to_study_use_case,
        search_phrase_contexts_use_case=search_phrase_contexts_use_case,
        suggest_phrases_to_study_use_case=suggest_phrases_to_study_use_case,
    )
    redis_context_manager = RedisContextManager(redis=redis)
    agent = Agent(
        skill_classifier=skill_classifier,
        context_manager=redis_context_manager,
    )

    return agent
