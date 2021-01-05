from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase
from infrastructure.bot.interfaces import UserRequest
from millet import Skill


class AddPhraseToStudySkill(Skill):

    def __init__(self, save_phrase_to_study_usecase: SavePhraseToStudyUsecase):
        self._save_phrase_to_study_usecase = save_phrase_to_study_usecase

        super().__init__()

    def start(self, initial_message: UserRequest):
        self._save_phrase_to_study_usecase.execute(
            chat_id=initial_message.chat_id,
            source_phrase=initial_message.data['source_phrase'],
            target_phrase=initial_message.data['target_phrase'],
        )
        self.say('Связка {} - {} добавлено на изучение'.format(
            initial_message.data['source_phrase'],
            initial_message.data['target_phrase'],
        ))
