from bot.agent.skill_classifier import SkillClassifier
from millet import Agent
from millet.context import RedisContextManager
from redis_client import redis_client


def create_agent() -> Agent:
    skill_classifier = SkillClassifier()
    redis_context_manager = RedisContextManager(redis=redis_client)
    agent = Agent(
        skill_classifier=skill_classifier,
        context_manager=redis_context_manager,
    )
    return agent
