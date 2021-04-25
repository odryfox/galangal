import json
import uuid
from typing import Optional

from domain.interfaces import ILearnPhrasesDAO
from redis import Redis


class RedisLearnPhrasesDAO(ILearnPhrasesDAO):

    def __init__(self, redis: Redis):
        self._redis = redis

    def _generate_key(self, chat_id: str) -> str:
        return f'learn.{chat_id}'

    def save_translate(self, chat_id: str, translate: str) -> None:
        key = self._generate_key(chat_id)
        self._redis.set(key, translate)

    def get_translate(self, chat_id: str) -> Optional[str]:
        key = self._generate_key(chat_id)
        translate = self._redis.get(key)
        if translate:
            return translate.decode()
        return None
