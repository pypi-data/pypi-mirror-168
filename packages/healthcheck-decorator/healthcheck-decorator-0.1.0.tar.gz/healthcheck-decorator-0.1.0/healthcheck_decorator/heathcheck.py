import functools
from .monitor import HealthcheckedFunctionMonitor
from .conf import DEFAULT_TTL, REDIS_HOST, REDIS_DB, REDIS_PORT

monitor = HealthcheckedFunctionMonitor()
redis_client = monitor.get_cache_client()
default_ttl = DEFAULT_TTL


def healthcheck(func=None, key=None, ttl=default_ttl, cache_client=redis_client):
    if func is None:
        return functools.partial(healthcheck, key=key, ttl=ttl, cache_client=cache_client)
    cache_key = key or func.__name__
    monitor.set(cache_key)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        cache_client.set(cache_key, 'updated', ttl)
        return result

    return wrapper
