"""Connection interface for client connection :: its return the client connection depending upon the connection name
and there config
# @Author : kazijavedalam
"""

import constants as constants

from cosmos_client import CosmosDBClient
from mysql_client import MysqlDBClient
from redis_client import RedisClient
from postgre_sql_client import PostgreSQLClient
from clickhouse_client import ClickHouseClient
from validate_config import ValidateConfig
from redis_connection_pool import RedisConnPool
from cast_config import CastConfig


class ConnectionInterface(object):

    def __init__(self, name: str, config: dict, pool: dict):
        self.name = name
        self.config = config
        if name == constants.redis_name and pool is not None:
            validate_config = ValidateConfig.redis_config(self, pool)
            if len(validate_config) == 0:
                cast_cong = CastConfig.redispool(self, pool)
                self.client = self.get_redis_conn_pool(cast_cong).redis_pool
            else:
                self.client = validate_config
        if name == constants.redis_name and pool is None:
            validate_config = ValidateConfig.redis_config(self, config)
            if len(validate_config) == 0:
                cast_cong = CastConfig.redis(self, config)
                #print("cast config", cast_cong)
                self.client = self.get_redis_client(cast_cong, None).client
            else:
                self.client = validate_config
        elif name == constants.cosmos_name:
            validate_config = ValidateConfig.cosmos_config(self, config)
            if len(validate_config) == 0:
                self.client = self.get_cosmos_client(config)
            else:
                self.client = validate_config
        elif name == constants.mysql_name:
            validate_config = ValidateConfig.mysql_config(self, config)
            if len(validate_config) == 0:
                cast_cong = CastConfig.mysql(self, config)
                self.client = self.get_mysql_client(cast_cong)
                #self.change_to_equal(**config)
            else:
                self.client = validate_config
        elif name == constants.postgres_name:
            validate_config = ValidateConfig.postgres_config(self, config)
            if len(validate_config) == 0:
                self.client = self.get_postgres_client(config)
            else:
                self.client = validate_config
        elif name == constants.clickhouse_name:
            validate_config = ValidateConfig.clickhouse_config(self, config)
            if len(validate_config) == 0:
                self.client = self.get_clickhouse_client(config)
            else:
                self.client = validate_config

    @staticmethod
    def get_redis_client(config: dict, pool):
        return RedisClient(config, pool)

    @staticmethod
    def get_cosmos_client(config: dict):
        return CosmosDBClient(config["host"], config["master_key"])

    @staticmethod
    def get_mysql_client(config: dict):
        return MysqlDBClient(config)

    @staticmethod
    def get_postgres_client(config: dict):
        return PostgreSQLClient(config)

    @staticmethod
    def get_clickhouse_client(config: dict):
        return ClickHouseClient(config)

    # @staticmethod
    # def get_dwh_sql_client(config: dict):
    #     return DWHSQLClient(config)

    @staticmethod
    def get_redis_conn_pool(config: dict):
        return RedisConnPool(config)

    @staticmethod
    def change_to_equal(*args, **kwargs):
        print("fdsgdf", args)
