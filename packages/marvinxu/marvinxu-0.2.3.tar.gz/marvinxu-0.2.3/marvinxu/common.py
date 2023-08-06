import os
import re
import time
from datetime import datetime


def get_timestamp():
    """get current timestamp as in 'YYYYmmddHHMMSS'

    Returns:
        str: current timestamp
    """
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def convert_datestr(datestr, source_format, to_format="%Y-%m-%d"):
    """convert date string to another format

    Args:
        time_str (str): source date string
        source_format (str): source date format
        to_format (str, optional): target date format. Defaults to "%Y-%m-%d".

    Returns:
        str: target date string
    """
    return datetime.strptime(datestr, source_format).strftime(to_format)


def get_localdate():
    """get local date string

    Returns:
        str: date in format 'YYYY年mm月dd日'
    """
    return time.strftime("%Y年%m月%d日", time.localtime())


def make_folder(base_path: str):
    """make a folder named current timestamp

    Args:
        base_path (str): base directory

    Returns:
        str: folder path
    """
    fold_name = get_timestamp()
    fold_path = os.path.join(base_path, fold_name)
    os.mkdir(fold_path)
    return fold_path


def is_valid_idcard(idcard):
    """check if a idcard num is valid

    Args:
        idcard (str): idcard num to check

    Returns:
        bool: is valid
    """
    IDCARD_REGEX = "[1-9][0-9]{14}([0-9]{2}[0-9X])?"

    idcard = str(idcard)

    if not re.match(IDCARD_REGEX, idcard):
        return False

    try:
        items = [int(item) for item in idcard[:-1]]
    except:
        return False
    else:
        ## 加权因子表
        factors = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)

        ## 计算17位数字各位数字与对应的加权因子的乘积
        copulas = sum([a * b for a, b in zip(factors, items)])

        ## 校验码表
        ckcodes = ("1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2")

        return ckcodes[copulas % 11].upper() == idcard[-1].upper()


def filter_none(dict: dict):
    """filter out None in a dict

    Args:
        dict (dict): dict to be filtered

    Returns:
        dict: new dict
    """
    return {k: v for (k, v) in dict.items() if v is not None}


def get_files(directory, entry=False):
    flag = entry

    def get_res(entry):
        return entry if flag else entry.path

    path = os.path.abspath(directory)
    result = list()
    for entry in os.scandir(path):
        if entry.is_dir():
            result = result + get_files(get_res(entry), flag)
        else:
            result.append(get_res(entry))
    return result


def change_file_ext(filename, ext):
    return os.path.splitext(filename)[0] + ext


__all__ = [
    "get_timestamp",
    "convert_datestr",
    "get_localdate",
    "make_folder",
    "is_valid_idcard",
    "filter_none",
    "get_files",
    "change_file_ext",
]
