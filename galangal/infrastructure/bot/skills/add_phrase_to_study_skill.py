from infrastructure.bot.interfaces import UserRequest
from millet import Skill


class AddPhraseToStudySkill(Skill):

    def start(self, initial_message: UserRequest):
        self.say('Слово {} добавлено на изучение'.format(initial_message.data))
