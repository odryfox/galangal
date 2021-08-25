from unittest import mock

from domain.agent.skills.phrase_search_skill import PhraseSearchSkill
from domain.entities import UserRequest


class TestPhraseSearchSkill:

    def setup_method(self):
        self.search_phrase_usages_in_different_languages_usecase_mock = mock.Mock()

        self.skill = PhraseSearchSkill(
            search_phrase_usages_in_different_languages_usecase=self.search_phrase_usages_in_different_languages_usecase_mock,
        )
        self.chat_id = '100500'

    @mock.patch.object(PhraseSearchSkill, 'say')
    def test(self, say_mock):
        search_phrases_response = mock.Mock(phrase_usages_in_different_languages=mock.Mock())
        self.search_phrase_usages_in_different_languages_usecase_mock.execute.return_value = search_phrases_response

        user_request = UserRequest(
            chat_id=self.chat_id,
            message='I will be back',
            signal=None,
            phrase_to_study=None,
        )
        self.skill.execute(initial_message=user_request)

        self.search_phrase_usages_in_different_languages_usecase_mock.execute.assert_called_once_with(
            message=user_request.message
        )

        say_mock.assert_called_once_with(search_phrases_response)

    @mock.patch.object(PhraseSearchSkill, 'say')
    def test_not_found(self, say_mock):
        search_phrases_response = mock.Mock(phrase_usages_in_different_languages=[])
        self.search_phrase_usages_in_different_languages_usecase_mock.execute.return_value = search_phrases_response

        user_request = UserRequest(
            chat_id=self.chat_id,
            message='I will be back',
            signal=None,
            phrase_to_study=None,
        )
        self.skill.execute(initial_message=user_request)

        self.search_phrase_usages_in_different_languages_usecase_mock.execute.assert_called_once_with(
            message=user_request.message
        )

        say_mock.assert_called_once_with('Фраз не найдено')
