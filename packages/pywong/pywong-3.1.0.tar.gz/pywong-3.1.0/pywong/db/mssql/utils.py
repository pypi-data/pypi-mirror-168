import pymssql
from pywong.db.mssql.settings import OPTION


class DbHelper:
    """MsSQL工具类"""

    def __init__(self, server="127.0.0.1", user=None, password=None, database=None, port=1433, charset='utf8', autocommit=True, as_dict=True):
        """构造函数"""
        self.database = database
        self.conn = pymssql.connect(
            server=server,
            port=str(port),
            user=user,
            password=password,
            database=database,
            charset=charset,
            autocommit=autocommit,
            as_dict=as_dict
        )
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

    def execute(self, sql, option=OPTION.select, d_list=None):
        """获取SQL执行结果：含增删改查"""
        if option == OPTION.select:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        elif option == OPTION.insertMany:
            return self.cursor.executemany(sql, d_list)
        else:
            return self.cursor.execute(sql)
