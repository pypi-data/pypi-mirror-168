# @Author : kazijavedalam
import redis


class RedisConnPool(object):
    def __init__(self, config: dict):
        try:
            self.redis_pool = redis.ConnectionPool(**config)
        except Exception as err:
            self.redis_pool = err
