import fire
from domain.services import RegexLanguageService
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot import create_agent
from infrastructure.cli.config import Config
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from millet import Agent


class CLI:
    def __init__(self, agent: Agent):
        self._agent = agent

    def search(self):
        while True:
            message = input()
            chat_id = 'console'
            answers = self._agent.query(message, chat_id)
            for answer in answers:
                print(answer)


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

        agent = create_agent(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        )

        self.cli = CLI(agent=agent)

    def run(self):
        fire.Fire(self.cli)
