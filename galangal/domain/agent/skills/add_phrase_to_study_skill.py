from domain.entities import UserRequest
from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase
from millet import Skill


class AddPhraseToStudySkill(Skill):

    def __init__(self, save_phrase_to_study_usecase: SavePhraseToStudyUsecase):
        self.save_phrase_to_study_usecase = save_phrase_to_study_usecase

        super().__init__()

    def start(self, initial_message: UserRequest):
        self.save_phrase_to_study_usecase.execute(
            chat_id=initial_message.chat_id,
            source_phrase=initial_message.phrase_to_study.source_phrase,
            target_phrase=initial_message.phrase_to_study.target_phrase,
        )
        self.say('Связка {} - {} добавлено на изучение'.format(
            initial_message.phrase_to_study.source_phrase,
            initial_message.phrase_to_study.target_phrase,
        ))
