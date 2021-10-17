from bot.agent import create_agent
from bot.constants import ActionType
from bot.markdown import Action
from redis_client import Redis


def test_agent(redis: Redis):
    action = Action(action_type=ActionType.GREETING, params={})
    agent = create_agent()
    answers = agent.query(action, user_id='test')

    assert answers == ['Привет, я бот, который поможет тебе выучить язык быстро']
