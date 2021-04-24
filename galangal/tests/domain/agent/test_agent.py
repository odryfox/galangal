from unittest import mock

from domain.agent.agent import SkillClassifier, create_agent
from domain.entities import AddPhraseToStudySignal, UserRequest
from millet import Agent


class TestAgent:

    def setup_method(self):
        self.chat_id = '100500'

    def test_skill_classifier__message(self):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()
        phrase_dao = mock.Mock()

        skill_classifier = SkillClassifier(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
            phrase_dao=phrase_dao,
        )

        user_request = UserRequest(
            chat_id=self.chat_id,
            message='I will be back',
            signal=None,
            phrase_to_study=None,
        )

        skill_names = skill_classifier.classify(user_request)

        assert skill_names == ['PhraseSearchSkill']

    def test_skill_classifier__signal(self):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()
        phrase_dao = mock.Mock()

        skill_classifier = SkillClassifier(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
            phrase_dao=phrase_dao,
        )

        user_request = UserRequest(
            chat_id=self.chat_id,
            message=None,
            signal=AddPhraseToStudySignal(),
            phrase_to_study=None,
        )

        skill_names = skill_classifier.classify(user_request)

        assert skill_names == ['AddPhraseToStudySkill']

    @mock.patch('domain.agent.agent.SkillClassifier')
    def test_create_agent(self, skill_classifier_mock):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()
        phrase_dao = mock.Mock()

        agent = create_agent(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
            phrase_dao=phrase_dao
        )

        assert isinstance(agent, Agent)
        skill_classifier_mock.assert_called_once_with(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
            phrase_dao=phrase_dao,
        )
