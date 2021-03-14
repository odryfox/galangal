from unittest import mock

from domain.agent.skills.add_phrase_to_study_skill import AddPhraseToStudySkill
from domain.entities import AddPhraseToStudySignal, PhraseToStudy, UserRequest
from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase


class TestAddPhraseToStudySkill:

    @classmethod
    def setup_class(cls):
        cls.save_phrase_to_study_usecase_mock = mock.Mock(
            spec=SavePhraseToStudyUsecase,
        )
        cls.skill = AddPhraseToStudySkill(
            save_phrase_to_study_usecase=cls.save_phrase_to_study_usecase_mock
        )
        cls.chat_id = '100500'

    @mock.patch.object(AddPhraseToStudySkill, 'say')
    def test(self, say_mock):
        user_request = UserRequest(
            chat_id=self.chat_id,
            message=None,
            signal=AddPhraseToStudySignal(),
            phrase_to_study=PhraseToStudy(
                source_phrase='source_phrase',
                target_phrase='target_phrase',
            ),
        )
        self.skill.start(initial_message=user_request)

        self.save_phrase_to_study_usecase_mock.execute.assert_called_once_with(
            chat_id=self.chat_id,
            source_phrase='source_phrase',
            target_phrase='target_phrase',
        )

        say_mock.assert_called_once_with(
            'Связка source_phrase - target_phrase добавлено на изучение'
        )
