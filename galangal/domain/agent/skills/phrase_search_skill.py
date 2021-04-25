from domain.entities import UserRequest
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from millet import BaseSkill


class PhraseSearchSkill(BaseSkill):

    def __init__(self, search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase) -> None:
        self.search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase

    def start(self, initial_message: UserRequest):
        search_phrases_response = self.search_phrase_usages_in_different_languages_usecase.execute(
            message=initial_message.message
        )

        if not search_phrases_response.phrase_usages_in_different_languages:
            self.say('Фраз не найдено')
        else:
            self.say(search_phrases_response)
