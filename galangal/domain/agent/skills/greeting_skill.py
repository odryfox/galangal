from domain.entities import GreetingResponse, UserRequest
from millet import Skill


class GreetingSkill(Skill):

    def start(self, initial_message: UserRequest):
        self.say(GreetingResponse(text='Привет, я бот, который поможет тебе выучить язык быстро'))
