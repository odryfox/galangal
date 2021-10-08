from bot.agent.agent import create_agent
from bot.constants import ActionType
from bot.markdown import Action
from language.services import RecognizeLanguageService
from redis import Redis
from search_phrase_contexts.daos import PhraseContextsDAO
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase
from vocabulary_trainer.daos import PhraseToStudyDAO
from vocabulary_trainer.use_cases import (
    AddPhraseToStudyUseCase,
    SuggestPhrasesToStudyUseCase
)


def test_agent(redis: Redis):
    agent = create_agent(
        add_phrase_to_study_use_case=AddPhraseToStudyUseCase(
            phrase_to_study_dao=PhraseToStudyDAO(),
        ),
        search_phrase_contexts_use_case=SearchPhraseContextsUseCase(
            recognize_language_service=RecognizeLanguageService(),
            phrase_contexts_dao=PhraseContextsDAO(),
        ),
        suggest_phrases_to_study_use_case=SuggestPhrasesToStudyUseCase(),
        redis=redis,
    )

    action = Action(action_type=ActionType.GREETING, params={})
    answers = agent.query(action, user_id='test')

    assert answers == ['Привет, я бот, который поможет тебе выучить язык быстро']
