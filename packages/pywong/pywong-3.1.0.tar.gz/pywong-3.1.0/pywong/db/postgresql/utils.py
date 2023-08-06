import psycopg2
from pywong.db.postgresql.settings import OPTION, DEFAULT, DATABASES
import pandas as pd
from sqlalchemy import create_engine


class DbHelper:
    """PostgreSQL工具类"""

    def __init__(self, host="127.0.0.1", user=None, password=None, database=None, port=5432,
                 dsn=None, connection_factory=None, cursor_factory=None, **kwargs):
        """构造函数"""
        self.database = database
        self.conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=str(port),
                                     dsn=dsn, connection_factory=connection_factory, cursor_factory=cursor_factory,
                                     **kwargs)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """析构函数"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_conn(self):
        """获取连接"""
        return self.conn

    def get_cursor(self):
        """获取游标"""
        return self.cursor

    def execute(self, sql, option=OPTION.select, d_list=None, vars=None):
        """获取SQL执行结果：含增删改查"""
        if option == OPTION.select:
            self.cursor.execute(sql, vars)
            return self.cursor.fetchall()
        elif option == OPTION.insertMany:
            return self.cursor.executemany(sql, d_list)
        else:
            return self.cursor.execute(sql, vars)

    @staticmethod
    def execute_query_pd(sql):
        """获取SQL查询结果，pandas方式"""
        return pd.read_sql(sql, create_engine(f"postgresql://{DEFAULT['user']}:{DEFAULT['password']}@{DEFAULT['host']}:"
                                              f"{DEFAULT['port']}/{DATABASES['default_database']}"))
