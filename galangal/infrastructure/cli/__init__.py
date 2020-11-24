import fire
from domain.services import RegexLanguageService
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.cli.config import Config
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)


class CLI:
    def __init__(self, search_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase):
        self._search_usecase = search_usecase

    def search(self):
        while True:
            message = input()
            result = self._search_usecase.execute(message=message)
            print(result)


class App:

    def __init__(self, config: Config):
        regex_language_service = RegexLanguageService()

        phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
            language_service=regex_language_service,
        )

        search_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
            language_service=regex_language_service,
            phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
        )

        self.cli = CLI(search_usecase=search_usecase)

    def run(self):
        fire.Fire(self.cli)
