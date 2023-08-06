from datetime import datetime
import os

CURRENT_DATE = datetime.now()
YEAR = CURRENT_DATE.year
MONTH = CURRENT_DATE.month
DAY = CURRENT_DATE.day


def now(date_format='%Y-%m-%d-%H-%M-%S'):
    return datetime.now().strftime(date_format)


def path_exits(path):
    return os.path.exists(path)


def isdir(path):
    return os.path.isdir(path)


def scandir(path):
    return os.scandir(path)


def chdir(path):
    os.chdir(path)


def parent_dir(path):
    return os.path.dirname(path)


def joinpath(*args, **kwargs):
    return os.path.join(*args, **kwargs)
