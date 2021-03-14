import json
import uuid
from typing import Optional

from domain.interfaces import ICallbackDataDAO
from redis import Redis


class RedisCallbackDataDAO(ICallbackDataDAO):

    def __init__(self, redis: Redis):
        self._redis = redis

    def _generate_key(self) -> str:
        return str(uuid.uuid4())

    def save_data(self, data: dict) -> str:
        dumped_data = json.dumps(data)
        key = self._generate_key()
        self._redis.set(key, dumped_data)
        return key

    def load_data(self, key: str) -> Optional[dict]:
        dumped_data = self._redis.get(key)
        if dumped_data:
            data = json.loads(dumped_data)
        else:
            data = None
        return data
