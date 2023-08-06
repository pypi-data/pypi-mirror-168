
from retrying import retry
import redis


@retry(stop_max_attempt_number=3, wait_random_min=100, wait_random_max=1000)
def redis_connect(redis_config):
    return redis.Redis(**redis_config)

