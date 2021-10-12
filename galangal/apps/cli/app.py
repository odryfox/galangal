from bot.agent.agent import create_agent
from bot.messengers.cli import CLIProcessMessageService
from config import Config
from language.services import RecognizeLanguageService
from redis import Redis
from search_phrase_contexts.daos import PhraseContextsDAO
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase
from vocabulary_trainer.daos import PhraseToStudyDAO
from vocabulary_trainer.use_cases import (
    AddPhraseToStudyUseCase,
    SuggestPhrasesToStudyUseCase
)


class App:
    def __init__(self, config: Config):
        agent = create_agent(
            add_phrase_to_study_use_case=AddPhraseToStudyUseCase(
                phrase_to_study_dao=PhraseToStudyDAO(),
            ),
            search_phrase_contexts_use_case=SearchPhraseContextsUseCase(
                recognize_language_service=RecognizeLanguageService(),
                phrase_contexts_dao=PhraseContextsDAO(),
            ),
            suggest_phrases_to_study_use_case=SuggestPhrasesToStudyUseCase(),
            redis=Redis.from_url(config.REDIS_URL),
        )
        self.process_message_service = CLIProcessMessageService(
            agent=agent
        )

    def run(self):
        message = None
        while True:
            self.process_message_service.execute(message)
            message = input()

            if message in (':quit', ':q'):
                break


def create_app(config: Config):
    return App(config=config)
