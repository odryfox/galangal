from bot.markdown import Action
from millet import BaseSkill
from vocabulary_trainer.entities import PhraseToStudy
from vocabulary_trainer.use_cases import AddPhraseToStudyUseCase


class AddPhraseToStudySkill(BaseSkill):

    def __init__(self, add_phrase_to_study_use_case: AddPhraseToStudyUseCase):
        self.add_phrase_to_study_use_case = add_phrase_to_study_use_case

    def execute(self, message: Action) -> str:
        self.add_phrase_to_study_use_case.execute(
            chat_id=self.user_id,
            phrase_to_study=PhraseToStudy(
                source_language_phrase=message.params['source_language_phrase'],
                target_language_phrase=message.params['target_language_phrase'],
            ),
        )
        return 'Связка {} - {} добавлена на изучение'.format(
            message.params['source_language_phrase'],
            message.params['target_language_phrase'],
        )
