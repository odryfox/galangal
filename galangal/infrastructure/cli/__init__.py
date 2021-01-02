import fire
from domain.services import RegexLanguageService
from domain.usecases.phrase_to_study_usecases import (
    GetPhraseToStudyFromSearchUsecase
)
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot import create_agent
from infrastructure.bot.cli import CLIBot
from infrastructure.cli.config import Config
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)


class CLI:

    def __init__(self, cli_bot: CLIBot):
        self._cli_bot = cli_bot

    def search(self):
        while True:
            request = input()
            self._cli_bot.execute(request)


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

        get_phrases_to_study_from_search_usecase = GetPhraseToStudyFromSearchUsecase()

        agent = create_agent(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
        )

        cli_bot = CLIBot(agent=agent)

        self.cli = CLI(cli_bot=cli_bot)

    def run(self):
        fire.Fire(self.cli)
