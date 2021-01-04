from infrastructure.redis.callback_data_dao import RedisCallbackDataDAO
from infrastructure.web.config import TestEnvironmentConfig


class TestCallbackDataDAO:

    def setup_method(self):
        config = TestEnvironmentConfig()
        self._dao = RedisCallbackDataDAO(redis_url=config.REDIS_URL)

    def test_generate_key(self):
        key = self._dao._generate_key()

        assert key

    def test_get_set(self):
        data = {'1': 1}
        key = self._dao.save_data(data)
        actual_data = self._dao.load_data(key)

        assert actual_data == data
