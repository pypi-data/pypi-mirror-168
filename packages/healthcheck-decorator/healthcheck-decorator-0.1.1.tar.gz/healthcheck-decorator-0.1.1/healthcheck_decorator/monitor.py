import redis
from .conf import REDIS_HOST, REDIS_DB, REDIS_PORT


class HealthcheckedFunctionMonitor:
    healthchecked_function = []
    cache = None

    def __init__(self):
        self.cache = self.get_cache_client()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                HealthcheckedFunctionMonitor, cls).__new__(cls)
        return cls.instance

    def set(self, key):
        self.healthchecked_function.append(key)

    def get(self):
        return self.healthchecked_function

    def delete(self, key):
        if key == '*':
            self.healthchecked_function = []
        if self.healthchecked_function:
            del self.healthchecked_function[key]

    def get_cache_client(self):
        if not self.cache:
            self.cache = redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return self.cache
