from domain.constants import Language
from domain.interfaces import (
    ILanguageService,
    IPhraseUsagesInDifferentLanguagesService
)
from millet import Skill


class PhraseSearchSkill(Skill):

    def __init__(
        self,
        language_service: ILanguageService,
        phrase_usages_in_different_languages_service: IPhraseUsagesInDifferentLanguagesService,
    ) -> None:

        self._language_service = language_service
        self._phrase_usages_in_different_languages_service = phrase_usages_in_different_languages_service

        super().__init__()

    def _get_target_language(self, source_language: Language) -> Language:
        return Language.RU if source_language is Language.EN else Language.EN

    def start(self, initial_message: str):
        source_language = self._language_service.get_language(initial_message)
        target_language = self._get_target_language(source_language)

        phrase_usages_in_different_languages = self._phrase_usages_in_different_languages_service.search(
            phrase=initial_message,
            languages=[target_language],
            limit=5,
        )

        self.say(phrase_usages_in_different_languages)
