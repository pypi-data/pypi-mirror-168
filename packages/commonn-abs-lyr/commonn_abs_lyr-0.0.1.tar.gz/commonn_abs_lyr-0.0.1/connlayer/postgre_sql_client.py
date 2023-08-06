"""PostgreSql :: Client to get connection. When this code will be called it will return only the connection based on the config passed.
Will return exception in cases where config will have issues.
# @Author : kazijavedalam
"""
import psycopg2


class PostgreSQLClient(object):

    def __init__(self, config: dict):
        try:
            conn_string = "host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}".format(host=config["host.name"],
                                                                                         user=config["user"],
                                                                                         dbname=config["database"],
                                                                                         password=config["password"],
                                                                                         sslmode=config["ssl.mode"])
            self.client = psycopg2.connect(conn_string)
        except Exception as err:
            self.client = err
