from domain.usecases.phrase_to_study_usecases import (
    GetPhraseToStudyFromSearchUsecase
)
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from infrastructure.bot.interfaces import UserRequest
from millet import Skill


class PhraseSearchSkill(Skill):

    def __init__(
        self,
        search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
        get_phrases_to_study_from_search_usecase: GetPhraseToStudyFromSearchUsecase,
    ) -> None:

        self._search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase
        self._get_phrases_to_study_from_search_usecase = get_phrases_to_study_from_search_usecase

        super().__init__()

    def start(self, initial_message: UserRequest):
        phrase_usages_in_different_languages = self._search_phrase_usages_in_different_languages_usecase.execute(
            message=initial_message.message
        )

        phrases_to_study = self._get_phrases_to_study_from_search_usecase.execute(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
        )

        self.say(tuple([phrase_usages_in_different_languages, phrases_to_study]))
