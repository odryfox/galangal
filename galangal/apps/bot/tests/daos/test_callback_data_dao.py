import pytest
from _pytest.fixtures import FixtureRequest
from bot.daos import CallbackDataDAO
from redis import Redis


class TestCallbackDataDAO:

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, request: FixtureRequest, redis: Redis):
        self.redis = redis
        self.dao = CallbackDataDAO(redis=self.redis)

    def test_generate_key(self):
        key = self.dao._generate_key()

        assert key

    def test_get_set(self):
        data = {'1': 1}
        key = self.dao.save_data(data)
        actual_data = self.dao.load_data(key)

        assert actual_data == data
