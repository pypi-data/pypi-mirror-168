
from influxdb import DataFrameClient
from intelab_python_tool.tools.connect import ConnectError
from retrying import retry
from functools import wraps
from contextlib import contextmanager


def influxdb_query(influxdb_config: dict, types="r") -> any:
    """
    返回INFLUXDB连接和光标的装饰器, 使用方法如下：

    from intelab_python_tool.tools.connect.Influxdb import influxdb_query
    query_r = influxdb_query(influxdb_config: dict, 'r')    >> 获取数据
    query_w = influxdb_query(influxdb_config: dict, 'w')   >> 写入数据
    query_c = influxdb_query(influxdb_config: dict)    >> 返回客户端对象

    @query_r
    def get_data_test(read, number):
        sql = f'''SELECT * FROM TABLE_NAME LIMIT {number}'''
        result = read(sql)
        result = result.raw['series'][0]['values']
        ......

    @query_w
    def insert_data(write, data: dataframe, measurement, tags=None, **kwargs):
        result = write(df, measurement='operating_status', tags={
                        "device_id": monitoring_target_id,
                        "device_name": name.strip(),
                        "device_type": type,
                        "sensor_name": sensor_name
                        }, retention_policy='utilizations')
        ...

    :param types:
    :param influxdb_config:
    :return:
    """
    if influxdb_config.get("HOST"):
        format_influxdb_config = {
            'host': influxdb_config.get("HOST"),
            'port': influxdb_config.get("PORT"),
            'username': influxdb_config.get("USERNAME"),
            'password': influxdb_config.get("PASSWORD"),
            'database': influxdb_config.get("DATABASE")
        }
    else:
        format_influxdb_config = influxdb_config

    def _load_func(function):

        @wraps(function)
        @retry(stop_max_attempt_number=5, wait_random_min=100, wait_random_max=1000)
        def _execute(*args, **kwargs):
            with _connect(format_influxdb_config) as client:
                if types == "w":
                    return function(client.write_points, *args, **kwargs)
                elif types == 'r':
                    return function(client.query, *args, **kwargs)
                else:
                    return function(client, *args, **kwargs)
        return _execute

    return _load_func


@contextmanager
def _connect(influxdb_config: dict) -> any:
    """
    建立和influxdb的连接并返回客户端
    :param influxdb_config:
    :return:
    """
    try:
        client = DataFrameClient(**influxdb_config)
        yield client
    except ConnectError:
        raise ConnectError("influxdb连接错误, 请检查配置文件")
    except Exception as e:
        raise e


if __name__ == '__main__':
    influxdb_config = {
        'HOST': 'platform.jiandu-test.ilabservice.cloud',
        'PORT': 32406,
        'USERNAME': 'ilabservice',
        'PASSWORD': 'AqcDoDs[i[rWW4b+aSEw',
        'DATABASE': 'intelab'}

    query_r = influxdb_query(influxdb_config, 'r')

    @query_r
    def get_data(read):
        sql = '''select value from temperature where time > '2021-03-01 00:00:00' and time < '2022-07-20 00:00:00' limit 30 '''
        result = read(sql)
        # results = result.raw['series'][0]['values']
        # results = np.array(results)
        # results = results[:, -1]
        # if isinstance(results[0], str):
        #     results = [eval(i) for i in results]
        return result['temperature']['value']

    data = get_data()
    print(data)
