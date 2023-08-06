from pywong.db.mysql.utils import DbHelper as mysql_DbHelper
from pywong.db.mysql.settings import DEFAULT as mysql_DEFAULT, DATABASES as mysql_DATABASES, OPTION as mysql_OPTION

from pywong.db.postgresql.utils import DbHelper as pg_DbHelper
from pywong.db.postgresql.settings import DEFAULT as pg_DEFAULT, DATABASES as pg_DATABASES, OPTION as pg_OPTION

from pywong.db.mssql.utils import DbHelper as mssql_DbHelper
from pywong.db.mysql.settings import DEFAULT as mssql_DEFAULT, DATABASES as mssql_DATABASES, OPTION as mssql_OPTION

from pywong.db.settings import DATABASE_TYPE


# 获取数据库帮助类实例
def get_db_helper(db_type):
    mysql_helper = None
    pg_helper = None
    mssql_helper = None

    if (db_type == DATABASE_TYPE.MYSQL) or (db_type == DATABASE_TYPE.ALL):
        mysql_helper = mysql_DbHelper(host=mysql_DEFAULT['host'], user=mysql_DEFAULT['user'],
                                      password=mysql_DEFAULT['password'], port=mysql_DEFAULT['port'],
                                      database=mysql_DATABASES['default_database'])

    if (db_type == DATABASE_TYPE.POSTGRESQL) or (db_type == DATABASE_TYPE.ALL):
        pg_helper = pg_DbHelper(host=pg_DEFAULT['host'], user=pg_DEFAULT['user'],
                                password=pg_DEFAULT['password'], port=pg_DEFAULT['port'],
                                database=pg_DATABASES['default_database'])

    if (db_type == DATABASE_TYPE.SQLSERVER) or (db_type == DATABASE_TYPE.ALL):
        mssql_helper = mssql_DbHelper(server=mssql_DEFAULT['server'], user=mssql_DEFAULT['user'],
                                      password=mssql_DEFAULT['password'], port=mssql_DEFAULT['port'],
                                      database=mssql_DATABASES['default_database'])

    return mysql_helper, pg_helper, mssql_helper
