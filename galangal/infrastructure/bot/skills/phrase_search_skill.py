from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot.interfaces import UserRequest
from millet import Skill


class PhraseSearchSkill(Skill):

    def __init__(
        self,
        search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase
    ) -> None:

        self._search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase

        super().__init__()

    def start(self, initial_message: UserRequest):
        phrase_usages_in_different_languages = self._search_phrase_usages_in_different_languages_usecase.execute(
            message=initial_message.message
        )

        self.say(phrase_usages_in_different_languages)