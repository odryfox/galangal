from domain.entities import UserRequest
from domain.interfaces import IPhraseDAO
from millet import BaseSkill


class LearnPhrasesSkill(BaseSkill):

    def __init__(self, phrase_dao: IPhraseDAO):
        super().__init__()
        self._phrase_dao = phrase_dao
        self.count = 1

    def start(self, initial_message: UserRequest):
        phrase = self._phrase_dao.get_phrase(initial_message.chat_id)
        if not phrase:
            self.say('Нет слов для изучения')
            return
        self._phrase = phrase
        self.ask(question=f'{self.count}. {phrase.source_phrase}', direct_to=self.check)

    def check(self, answer: UserRequest):
        if answer.message == self._phrase.target_phrase:
            self.say(f'{self.count}. Молодчик')
        else:
            self.say(f'{self.count}. Ошибка. Правильный ответ: {self._phrase.target_phrase}')

        self.count += 1
        if self.count <= 3:
            self.start(answer)
        else:
            self.say('Тренировка завершена')
