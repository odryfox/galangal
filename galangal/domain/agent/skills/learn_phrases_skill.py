from domain.entities import UserRequest
from domain.interfaces import IPhraseDAO
from millet import Skill


class LearnPhrasesSkill(Skill):

    def __init__(self, phrase_dao: IPhraseDAO):
        super().__init__()
        self._phrase_dao = phrase_dao
        self.count = 3

    def start(self, initial_message: UserRequest):
        phrase = self._phrase_dao.get_phrase(initial_message.chat_id)
        if not phrase:
            self.say('Нет слов для изучения')
            return
        self._phrase = phrase
        self.ask(question=phrase.source_phrase, direct_to=self.check)

    def check(self, answer: UserRequest):
        if answer.message == self._phrase.target_phrase:
            self.say('Молодчик')
        else:
            self.say('Ошибка. Правильный ответ: {}'.format(self._phrase.target_phrase))

        self.count -= 1
        if self.count != 0:
            self.start(answer)
        else:
            self.say('Тренировка завершена')
