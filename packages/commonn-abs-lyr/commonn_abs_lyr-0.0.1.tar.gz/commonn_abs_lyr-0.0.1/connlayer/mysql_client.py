"""Mysql :: Client to get connection. When this code will be called it will return only the connection based on the config passed.
Will return exception in cases where config will have issues.
# @Author : kazijavedalam
"""

import mysql.connector


class MysqlDBClient(object):

    def __init__(self, config):
        try:
            self.client = mysql.connector.connect(**config)

        except Exception as err:
            print("error", err)
