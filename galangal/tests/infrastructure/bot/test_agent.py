from unittest import mock

from infrastructure.bot import (
    AddPhraseToStudySignal,
    AddPhraseToStudySkill,
    PhraseSearchSkill,
    UserRequest,
    _create_skill_classifier,
    create_agent
)
from millet import Agent


class TestAgent:

    def test_skill_classifier__message(self):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        get_phrases_to_study_from_search_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()

        skill_classifier = _create_skill_classifier(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        user_request = UserRequest(
            chat_id='100500',
            message='I will be back',
            signal=None,
            data={},
        )

        skills = skill_classifier(user_request)

        assert len(skills), 1

        skill = skills[0]
        assert isinstance(skill, PhraseSearchSkill)
        assert skill._search_phrase_usages_in_different_languages_usecase == search_phrase_usages_in_different_languages_usecase
        assert skill._get_phrases_to_study_from_search_usecase == get_phrases_to_study_from_search_usecase

    def test_skill_classifier__signal(self):
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        get_phrases_to_study_from_search_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()

        skill_classifier = _create_skill_classifier(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        user_request = UserRequest(
            chat_id='100500',
            message=None,
            signal=AddPhraseToStudySignal(),
            data={},
        )

        skills = skill_classifier(user_request)

        assert len(skills), 1

        skill = skills[0]
        assert isinstance(skill, AddPhraseToStudySkill)
        assert skill._save_phrase_to_study_usecase == save_phrase_to_study_usecase

    @mock.patch('infrastructure.bot._create_skill_classifier')
    def test_create_agent(self, create_skill_classifier_mock):
        skill_classifier = mock.Mock()
        create_skill_classifier_mock.return_value = skill_classifier
        search_phrase_usages_in_different_languages_usecase = mock.Mock()
        get_phrases_to_study_from_search_usecase = mock.Mock()
        save_phrase_to_study_usecase = mock.Mock()

        agent = create_agent(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )

        assert isinstance(agent, Agent)
        create_skill_classifier_mock.assert_called_once_with(
            search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
            get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
            save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        )
