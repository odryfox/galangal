from millet import BaseSkill


class GreetingSkill(BaseSkill):

    def execute(self, message: str):
        self.say('Привет, я бот, который поможет тебе выучить язык быстро')
