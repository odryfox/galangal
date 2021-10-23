import json
import uuid
from typing import Optional

from redis_client import redis_client


class CallbackDataDAO:

    def _generate_key(self) -> str:
        return str(uuid.uuid4())

    def save_data(self, data: dict) -> str:
        dumped_data = json.dumps(data)
        key = self._generate_key()
        redis_client.set(key, dumped_data)
        return key

    def load_data(self, key: str) -> Optional[dict]:
        dumped_data = redis_client.get(key)
        if dumped_data:
            data = json.loads(dumped_data)
        else:
            data = None
        return data
