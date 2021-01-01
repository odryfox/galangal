import fire
from domain.services import RegexLanguageService
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot import create_agent
from infrastructure.bot.cli import CLIBot
from infrastructure.bot.interfaces import IBot
from infrastructure.cli.config import Config
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from millet import Agent


class CLI:
    def __init__(self, agent: Agent, bot: IBot):
        self._agent = agent
        self._bot = bot

    def search(self):
        while True:
            request = input()
            user_request, chat_id = self._bot.parse_request(request)

            responses = self._agent.query(user_request, chat_id)

            self._bot.send_responses(responses, chat_id)


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

        bot = CLIBot()

        self.cli = CLI(agent=agent, bot=bot)

    def run(self):
        fire.Fire(self.cli)
