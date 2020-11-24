import fire
from domain.services import RegexLanguageService
from domain.skills import create_skill_classifier
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

        skill_classifier = create_skill_classifier(
            language_service=regex_language_service,
            phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
        )
        agent = Agent(skill_classifier=skill_classifier)

        self.cli = CLI(agent=agent)

    def run(self):
        fire.Fire(self.cli)
