from domain.entities import UserRequest
from domain.interfaces import ILearnPhrasesDAO, IPhraseDAO
from millet import BaseSkill


class LearnPhrasesSkill(BaseSkill):

    INITIAL_STATE_NAME = 'ask_phrase'

    def __init__(self, phrase_dao: IPhraseDAO, learn_phrases_dao: ILearnPhrasesDAO):
        self._phrase_dao = phrase_dao
        self._learn_phrases_dao = learn_phrases_dao

    def ask_phrase(self, initial_message: UserRequest):
        phrase = self._phrase_dao.get_phrase(initial_message.chat_id)
        if not phrase:
            self.say('Нет слов для изучения')
            return

        translate = phrase.target_phrase
        self._learn_phrases_dao.save_translate(
            chat_id=initial_message.chat_id,
            translate=translate,
        )

        self.ask(phrase.source_phrase, direct_to='check')

    def check(self, answer: UserRequest):
        if answer.signal:
            self.say('Обучение закончено')
            return

        translate = self._learn_phrases_dao.get_translate(answer.chat_id)
        if not translate:
            self.say('Произошла ошибка')
            return

        if answer.message.lower().strip() == translate.lower().strip():
            self.say('Верно')
        else:
            self.say(f'Ошибка. Правильный ответ: {translate}')

        self.ask_phrase(answer)
