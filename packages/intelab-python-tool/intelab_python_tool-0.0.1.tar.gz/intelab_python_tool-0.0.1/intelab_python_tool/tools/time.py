
import time
import dateutil.parser
from datetime import datetime, timedelta


def get_on_the_hour(times: any) -> datetime:
    """
    将输入时间的分秒舍去, 取整点
    :param times:
    :return:
    """
    if not isinstance(times, datetime):
        times = dateutil.parser.parse(times)
    return datetime(times.year, times.month, times.day, times.hour)


def datetime2str(times: datetime, _format='%Y-%m-%d %H:%M:%S') -> str:
    """
    将 datetime 格式的时间转化为 str 格式
    :param times:
    :param _format:
    :return:
    """
    return times.strftime(_format) if isinstance(times, datetime) else times


def str2datetime(times: str, _format='%Y-%m-%d %H:%M:%S') -> datetime:
    """
    将 str 格式的时间转化为 datetime 格式
    :param times:
    :param _format:
    :return:
    """
    return datetime.strptime(times, _format) if isinstance(times, str) else times


def str_utc2cst(times: str) -> str:
    """
    将 str 格式的 utc 时间转化为 str 格式的北京时间
    :param times:
    :return:
    """
    return datetime2str(str2datetime(times) + timedelta(hours=8))


def datetime2timestamp(times: datetime) -> int:
    """
    将 datetime 格式的时间转为 13 位毫秒时间戳
    :param times:
    :return:
    """
    return int(time.mktime(times.timetuple()) * 1000.0 + times.microsecond / 1000.0)


def timestamp2datetime(times: int) -> datetime:
    """
    将 13 位整数毫秒时间戳转化成 datetime 格式
    :param times:
    :return:
    """
    return datetime.fromtimestamp(times / 1000.0)

