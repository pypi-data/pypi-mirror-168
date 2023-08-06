"""ClickHouse :: Client to get connection. When this code will be called it will return only the connection based on the config passed.
Will return exception in cases where config will have issues.
# @Author : kazijavedalam
"""
from clickhouse_driver import Client


class ClickHouseClient(object):

    def __init__(self, config):
        try:
            self.client = Client(host=config["host"],
                                 user=config["user"],
                                 password=config["password"],
                                 secure=True,
                                 verify=False,
                                 database=config["database"],
                                 compression=True)

        except Exception as err:
            self.client = err
