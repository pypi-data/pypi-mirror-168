# coding=utf-8

import toml
import logging
from typing import Dict, List, Mapping
from exuse.expath import join, abspath, dirname, filename, isabs, isdir, list_files
from .const import APP_NAME


def _extract_unique_keys(rawdata: Mapping):
    '''遍历嵌套字典所有深度上的键，提取出键名唯一的键值对，即排除出现两次及以上键名的键值对'''
    qd = {}
    dup_keys = []

    def iterate(k, v):
        if isinstance(v, dict):
            for x, y in v.items():
                iterate(x, y)
        else:
            if qd.get(k) is not None:
                dup_keys.append(k)
            qd[k] = v

    for k, v in rawdata.items():
        iterate(k, v)

    for k in dup_keys:
        qd.pop(k)

    return qd


def get_nested_key(obj: dict, nested_key: str, nest_delimiter='.'):
    """从嵌套字典中按照嵌套键取出对应的值

    Args:
        obj (dict): 一个字典
        nested_key (str): 嵌套的键
        nest_delimiter (str, optional): 键嵌套的分隔符. Defaults to '.'.

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    keys = nested_key.split(nest_delimiter)
    tmp = obj
    for key in keys:
        tmp = tmp[key]
    return tmp


class EnvLoader:
    '''
    Memebers:
    - `rootdir`: project root dir
    - `env_file`: path of env.toml
    - `raw`: json object loaded from `env_file`
    '''
    graph_working_dir = f'/tmp/{APP_NAME}/graphs'

    def __init__(self, env_file: str = None, strict=False, checking_path=False):
        """
        Args:
            env_file (str, optional): 环境配置文件. 默认为项目根目录下的 env.toml 文件.
            strict (bool, optional): 是否启用严格验证. Defaults to False.
            启用严格验证时，如果查询的键在文件中未定义，抛出异常；否则返回键本身.
        """
        if env_file is None:
            logging.debug('not use any env file!')
            self.rootdir = None
            self.raw = {}
        else:
            logging.debug(f'use environments: {env_file}')
            self.rootdir = abspath(dirname(env_file))
            self.raw = toml.load(env_file)

        self.env_file = env_file
        self._uniq_kvs = _extract_unique_keys(self.raw)

        self.use_strict = strict
        self.checking_path = checking_path

        self.__registered_units: Dict[str, str] = None

    def __str__(self):
        return f'EnvLoader<{self.env_file}>'

    def get_raw(self, dotted_key: str):
        if self.rootdir is None:
            raise Exception('no env file used!')
        # 直接通过单键取出值，自动进行深层遍历
        if '.' not in dotted_key:
            try:
                return self._uniq_kvs[dotted_key]
            except KeyError:
                raise KeyError(f'Undefined or multi-defined env key "{dotted_key}"')
        # 嵌套的键
        else:
            try:
                return get_nested_key(self.raw, dotted_key)
            except KeyError:
                raise KeyError(f'Undefined env key "{dotted_key}"')

    def fix_path(self, _path: str) -> str:
        """
        从环境文件中取出的路径如果是相对路径，则需要修复为相对于项目根目录的绝对路径

        Args:
            _path (str): 相对路径或者绝对路径，绝对路径不进行修复

        Returns:
            str: 绝对路径
        """
        if _path.startswith('#') or _path.startswith('/') or isabs(_path):
            return _path
        else:
            return abspath(join(self.rootdir, _path))

    def get_path(self, dotted_key: str) -> str:
        v = None
        try:
            return self.get_raw(dotted_key)
        except KeyError:
            return dotted_key

    def get_path_list(self, dotted_key: str, default=[]) -> List[str]:
        arr = None
        try:
            arr = self.get_raw(dotted_key)
        except KeyError:
            arr = default

        return [self.fix_path(x) for x in arr]

    @property
    def registered_module_units(self):
        """通过环境文件注册的模块单元"""
        if self.env_file is None:
            raise Exception('no env file used!')
        if self.__registered_units is None:
            #
            default_units = {}
            default_unit_dir = join(dirname(__file__), 'units')
            for x in list_files(default_unit_dir, ['json', 'toml']):
                default_units[filename(x)] = x
            #
            module_units = {}
            for item in self.get_path_list('registered_units'):
                if not isdir(item):
                    raise Exception(f'register units failed from {item}')
                for x in list_files(item):
                    name = filename(x)
                    if name in module_units and abspath(x) != module_units[name]:
                        raise RuntimeError(f'Duplicate module unit found: {name}')
                    module_units[name] = abspath(x)

            for k, p in default_units.items():
                if k not in module_units:
                    module_units[k] = p

            self.__registered_units = module_units
        return self.__registered_units

    def executor(self, key: str) -> str:
        return self.get_path('executors.%s' % key)

    def script(self, key: str) -> str:
        return self.get_path(f'scripts.{key}')
