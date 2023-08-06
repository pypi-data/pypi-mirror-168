# @Author : kazijavedalam
# from dwh_sql_client import DWHSQLClient
from redis_client import RedisClient
from redis_connection_pool import RedisConnPool
from mysql_client import MysqlDBClient
from connection_interface import ConnectionInterface

if __name__ == '__main__':
    config = {'driver': '{ODBC Driver 13 for SQL Server}',
              'host': 'mccia.database.windows.net',
              'port': '1433',
              'database': 'mccia',
              'user': 'biguser',
              'password': 'l0Adus3r'
              }
    mysql_qa = {
        'user': 'root',
        'password': 'root@123',
        'host': '127.0.0.1',
        'database': 'cifeed'
    }
    redis_config = {'host': '127.0.0.1',
                    'port': '6379',
                    'database': 'db0'
                    }
    # df = DWHSQLClient(config)
    # print(df)
    # pool = RedisConnPool(redis_config)
    #rd = RedisClient(redis_config, None)
    rd_f = ConnectionInterface("redis", None, redis_config)
    #rd = rd.client
    print("abc", rd_f.client)
    #keys = rd_f.client.get("layer")
    #print("abc", keys)
    #ms_ql = ConnectionInterface("mysql", mysql_qa, None)
    #ms_ql = MysqlDBClient(mysql_qa)
    # ms_ql = ms_ql.client
    # print(ms_ql)
    # query = "SELECT * from feed_link"
    # mysql_cur = ms_ql.client.cursor()
    # mysql_cur.execute(query)
    # row = mysql_cur.fetchone()
    # print("Current date is: {0}".format(row[0]))
    # #
    # # # Close connection
    # mysql_cur.close()
