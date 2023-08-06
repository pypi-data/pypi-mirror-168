"""Redis :: Client to get connection. When this code will be called it will return only the connection based on the config passed.
Will return exception in cases where config will have issues.
# @Author : kazijavedalam
"""
import redis


class RedisClient(object):

    def __init__(self, config: dict, pool):
        try:
            if pool is not None:
                self.client = redis.Redis(connection_pool=pool)

            elif config and pool is None:
                self.client = redis.Redis(**config)
            # print(redis_connection)
            # keys = redis_connection.keys('*')
            # print(keys)
            # vals = redis_connection.mget(keys)
            # kv = zip(keys, vals)
            # print(vals)
        except Exception as err:
            self.client = err
