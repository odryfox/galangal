from unittest import mock

from infrastructure.bot import (
    AddPhraseToStudySignal,
    AddPhraseToStudySkill,
    UserRequest
)


class TestAddPhraseToStudySkill:

    @classmethod
    def setup_class(cls):
        cls.skill = AddPhraseToStudySkill()

    @mock.patch.object(AddPhraseToStudySkill, 'say')
    def test(self, say_mock):
        user_request = UserRequest(
            message=None,
            signal=AddPhraseToStudySignal(),
            data='data',
        )
        self.skill.start(initial_message=user_request)

        say_mock.assert_called_once_with(
            'Слово data добавлено на изучение'
        )
