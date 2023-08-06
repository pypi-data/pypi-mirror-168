import os
import sys
import shutil
from glob import glob
from sparrow.path import rel_to_abs
import orjson
import pickle
from typing import Union, List, Dict
from .core import broadcast


@broadcast
def rm(PATH):
    """Enhanced rm, support for regular expressions"""

    def _rm(path):
        """remove path"""
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            else:
                print(f"{path} is illegal.")

    path_list = glob(PATH)
    for path in path_list:
        _rm(path)


def path(string: str) -> str:
    """Adaptive to different platforms"""
    platform = sys.platform.lower()
    if platform in ("linux", "darwin"):
        return string.replace("\\", "/")
    elif platform in ("win", "win32"):
        return string.replace("/", "\\")
    else:
        return string


def save(filename, file):
    with open(filename, "wb") as fw:
        pickle.dump(file, fw)


def load(filename):
    with open(filename, "rb") as fi:
        file = pickle.load(fi)
    return file


def json_load(filepath: str, rel=False):
    abs_path = rel_to_abs(filepath, parents=1) if rel else filepath
    with open(abs_path, 'rb') as f:
        return orjson.loads(f.read())


def json_dump(data: Union[List, Dict], filepath: str, rel=False, indent_2=False):
    orjson_option = 0
    if indent_2:
        orjson_option = orjson.OPT_INDENT_2
    abs_path = rel_to_abs(filepath, parents=1) if rel else filepath
    with open(abs_path, 'wb') as f:
        f.write(orjson.dumps(data, option=orjson_option))

def yaml_dump(filepath, data, rel_path=False):
    abs_path = rel_to_abs(filepath, parents=1) if rel_path else filepath
    from yaml import dump

    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    with open(abs_path, "w", encoding="utf-8") as fw:
        fw.write(dump(data, Dumper=Dumper, allow_unicode=True, indent=4))


def yaml_load(filepath, rel_path=False):
    abs_path = rel_to_abs(filepath, parents=1) if rel_path else filepath
    from yaml import load

    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(abs_path, "r", encoding="utf-8") as stream:
        #     stream = stream.read()
        content = load(stream, Loader=Loader)
    return content
