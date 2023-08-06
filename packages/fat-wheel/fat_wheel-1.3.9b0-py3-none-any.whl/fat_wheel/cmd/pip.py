# https://pip.pypa.io/en/latest/user_guide/#fast-local-installs
import os
from typing import List

INSTALL_PKG_IN_DIR_CMD = "pip install -r requirements.txt -t ."
DOWNLOAD_WHEEL_CMD = "pip download -r requirements.txt --dest {deps} --no-cache"
FAT_WHEEL_INSTALL = "pip download -r requirements.txt --dest deps --no-cache"
BUILD_CMD = "python setup.py {build_options}"
INSTALL_LOCAL_PKG_CMD = "python -m pip install --no-index --find-links=deps -r requirements.txt"


def download_wheel(path):
    __execute(DOWNLOAD_WHEEL_CMD.format(deps=os.path.join(path, "deps")))


def fat_wheel_install():
    __execute(FAT_WHEEL_INSTALL)


def install():
    __execute(BUILD_CMD.format(build_options="install"))


def build(options: List[str]):
    build_option_str = " ".join(options)
    __execute(BUILD_CMD.format(build_options=build_option_str))


def __execute(cmd):
    dir_path = f"~{os.path.basename(os.getcwd())}"
    print(f"{dir_path}> {cmd}")
    os.system(cmd)
