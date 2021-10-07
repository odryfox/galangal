from millet import BaseSkill


class GreetingSkill(BaseSkill):

    def execute(self, message: str) -> str:
        return 'Привет, я бот, который поможет тебе выучить язык быстро'
