from domain.agent import create_agent
from domain.services import RegexLanguageService
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase
from infrastructure.cli.bot import CLIBot
from infrastructure.cli.config import Config
from infrastructure.db.connection import DB
from infrastructure.db.phrase_dao import DBPhraseDAO
from infrastructure.third_party.reverso import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)


class App:

    def __init__(self, config: Config):

        regex_language_service = RegexLanguageService()
        phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
            language_service=regex_language_service,
        )
        search_phrase_usages_in_different_languages_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
            language_service=regex_language_service,
            phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
        )

        db = DB(url=config.DATABASE_URL)
        session = db.create_session()
        phrase_dao = DBPhraseDAO(session=session)
        save_phrase_to_study_usecase = SavePhraseToStudyUsecase(phrase_dao=phrase_dao)

        agent = create_agent(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        self.cli_bot = CLIBot(agent=agent)

    def run(self):
        while True:
            request = input()
            self.cli_bot.process_request(request)


def create_app(config: Config) -> App:
    return App(config=config)
