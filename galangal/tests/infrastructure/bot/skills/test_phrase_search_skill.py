from unittest import mock

from infrastructure.bot import PhraseSearchSkill, UserRequest
from infrastructure.bot.interfaces import SearchPhrasesResponse


class TestPhraseSearchSkill:

    def setup_method(self):
        self.search_phrase_usages_in_different_languages_usecase_mock = mock.Mock()
        self.get_phrases_to_study_from_search_usecase_mock = mock.Mock()

        self.skill = PhraseSearchSkill(
            search_phrase_usages_in_different_languages_usecase=self.search_phrase_usages_in_different_languages_usecase_mock,
            get_phrases_to_study_from_search_usecase=self.get_phrases_to_study_from_search_usecase_mock,
        )

    @mock.patch.object(PhraseSearchSkill, 'say')
    def test(self, say_mock):
        phrase_usages_in_different_languages = mock.Mock()
        self.search_phrase_usages_in_different_languages_usecase_mock.execute.return_value = phrase_usages_in_different_languages

        phrases_to_study = mock.Mock()
        self.get_phrases_to_study_from_search_usecase_mock.execute.return_value = phrases_to_study

        user_request = UserRequest(
            message='I will be back',
            signal=None,
            data={},
        )
        self.skill.start(initial_message=user_request)

        self.search_phrase_usages_in_different_languages_usecase_mock.execute.assert_called_once_with(
            message=user_request.message
        )

        self.get_phrases_to_study_from_search_usecase_mock.execute.assert_called_once_with(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
        )

        response = SearchPhrasesResponse(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            phrases_to_study=phrases_to_study,
        )
        say_mock.assert_called_once_with(response)
