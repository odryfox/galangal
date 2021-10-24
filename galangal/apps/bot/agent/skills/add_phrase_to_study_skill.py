from bot.markdown import Action
from millet import BaseSkill
from vocabulary_trainer.entities import PhraseToStudy
from vocabulary_trainer.use_cases import create_add_phrase_to_study_use_case


class AddPhraseToStudySkill(BaseSkill):

    def execute(self, message: Action, user_id: str) -> str:
        add_phrase_to_study_use_case = create_add_phrase_to_study_use_case()
        add_phrase_to_study_use_case.execute(
            chat_id=user_id,
            phrase_to_study=PhraseToStudy(
                source_language_phrase=message.params['source_language_phrase'],
                target_language_phrase=message.params['target_language_phrase'],
            ),
        )
        return 'Связка {} - {} добавлена на изучение'.format(
            message.params['source_language_phrase'],
            message.params['target_language_phrase'],
        )
