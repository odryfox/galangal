from unittest import mock

from infrastructure.bot import (
    AddPhraseToStudySignal,
    AddPhraseToStudySkill,
    PhraseSearchSkill,
    SkillClassifier,
    UserRequest,
    create_agent
)
from millet import Agent


class TestAgent:

    def setup_method(self):
        self.chat_id = '100500'

    def test_skill_classifier__message(self):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        get_phrases_to_study_from_search_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()

        skill_classifier = SkillClassifier(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        user_request = UserRequest(
            chat_id=self.chat_id,
            message='I will be back',
            signal=None,
            phrase_to_study=None,
        )

        skills = skill_classifier.classify(user_request)

        assert len(skills), 1

        skill = skills[0]
        assert isinstance(skill, PhraseSearchSkill)
        assert skill._search_phrase_usages_in_different_languages_usecase == search_phrase_usages_in_different_languages_usecase
        assert skill._get_phrases_to_study_from_search_usecase == get_phrases_to_study_from_search_usecase

    def test_skill_classifier__signal(self):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        get_phrases_to_study_from_search_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()

        skill_classifier = SkillClassifier(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        user_request = UserRequest(
            chat_id=self.chat_id,
            message=None,
            signal=AddPhraseToStudySignal(),
            phrase_to_study=None,
        )

        skills = skill_classifier.classify(user_request)

        assert len(skills), 1

        skill = skills[0]
        assert isinstance(skill, AddPhraseToStudySkill)
        assert skill._save_phrase_to_study_usecase == save_phrase_to_study_usecase

    @mock.patch('infrastructure.bot.SkillClassifier')
    def test_create_agent(self, skill_classifier_mock):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        get_phrases_to_study_from_search_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()

        agent = create_agent(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        assert isinstance(agent, Agent)
        skill_classifier_mock.assert_called_once_with(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )
