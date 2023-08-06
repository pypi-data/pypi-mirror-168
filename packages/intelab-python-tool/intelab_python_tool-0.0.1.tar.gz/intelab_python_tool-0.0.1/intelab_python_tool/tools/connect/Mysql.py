
from contextlib import contextmanager
import pymysql as mysql
from retrying import retry
from functools import wraps


def mysql_query(mysql_config: dict) -> any:
    """
    返回MYSQL连接和光标的装饰器, 使用方法如下：

    from intelab_python_tool.tools.connect.mysql import mysql_query
    query = mysql_query(mysql_config: dict)

    @query
    def get_data_test(cursor, connection, number):
        sql = f'''SELECT * FROM TABLE_NAME LIMIT {number}'''
        ......

    :param mysql_config:
    :return:
    """
    if mysql_config.get("HOST"):
        format_mysql_config = {
            'host': mysql_config.get("HOST"),
            'port': mysql_config.get("PORT"),
            'user': mysql_config.get("USERNAME"),
            'password': mysql_config.get("PASSWORD"),
            'database': mysql_config.get("DATABASE")
        }
    else:
        format_mysql_config = mysql_config

    def _load_func(function):

        @wraps(function)
        @retry(stop_max_attempt_number=5, wait_random_min=100, wait_random_max=1000)
        def _execute(*args, **kwargs):
            with _connect(format_mysql_config) as (cursor, connection):
                return function(cursor, connection, *args, **kwargs)
        return _execute

    return _load_func


@contextmanager
def _connect(mysql_config: dict) -> any:
    """
    建立和 mysql 的连接
    :param mysql_config:
    :return: mysql的连接和光标, 或者 error
    """
    connection = None

    try:
        connection = mysql.connect(**mysql_config)
        cursor = connection.cursor()
        yield cursor, connection
    except Exception as e:
        raise e
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    mysql_config = {
        "HOST": '47.101.208.180',
        "PORT": 32309,
        "USERNAME": 'root',
        "PASSWORD": 'iLabService123',
        "DATABASE": 'asset'
    }

    query = mysql_query(mysql_config)

    @query
    def get_asset_model_test(cursor, conn):
        sql = '''select * from t_ai_asset_model limit 10'''
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    a = get_asset_model_test()
    print(a)