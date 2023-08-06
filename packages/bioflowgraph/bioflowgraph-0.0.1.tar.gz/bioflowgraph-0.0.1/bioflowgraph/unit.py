# coding=utf-8

from collections import OrderedDict
from exuse.extypings import Dict, List
from exuse.expath import filename, exists, get_path_by_filename
from exuse.exio import read_jsonlike_file

from bioflowgraph.const import SHELL_DIR, STDXXX_DIR

from .env import EnvLoader


class Unit(object):
    """one unit, one program command!"""

    def __init__(self, name: str, configs: dict, env: EnvLoader):
        self.name = name
        self.raw = configs
        self.env = env
        self.stdout_key = 'STDOUT'
        self.stderr_key = 'STDERR'

        raw_params = OrderedDict({})
        is_stdout_defined = False
        is_stderr_defined = False
        for pd in self.raw.get('parameters', []):
            if pd['name'] == '':
                raise KeyError('Parameter name cannot be empty')
            if raw_params.get(pd['name']):
                raise KeyError(f'Duplicate parameter name: {pd["name"]}')
            raw_params[pd['name']] = pd

            pt = pd.get('type', 'str')
            if not is_stdout_defined and pt == 'stdout':
                is_stdout_defined = True
                self.stdout_key = pd['name']
            if not is_stderr_defined and pt == 'stderr':
                is_stderr_defined = True
                self.stderr_key = pd['name']

        if is_stdout_defined is False:
            raw_params['STDOUT'] = {'name': 'STDOUT', 'type': 'stdout', 'default': '%s/${TaskName}.sh.out' % STDXXX_DIR}
        if is_stderr_defined is False:
            raw_params['STDERR'] = {'name': 'STDERR', 'type': 'stderr', 'default': '%s/${TaskName}.sh.err' % STDXXX_DIR}

        self.raw_params = raw_params
        self.__params = None

    def __str__(self) -> str:
        return f'Unit<{self.name}>'

    @property
    def executor(self) -> str:
        _executor = self.raw.get('executor')
        # 模块名可以包含 executor 和 subexecutor 的信息，例如 samtools.view
        # 如果配置文件中没有提供 executor 则使用模块名作为 executor 名称
        if _executor is None:
            _executor = self.name.split('.')[0]

        if not exists(_executor):
            _executor = self.env.get_path(_executor)

        return _executor

    @property
    def sub_executor(self) -> str:
        _sub_executor = self.raw.get('sub_executor')
        if _sub_executor is None and '.' in self.name:
            _sub_executor = self.name.split('.')[1]
        return _sub_executor

    @property
    def param_names(self) -> List[str]:
        return list(self.raw_params.keys())

    @property
    def params(self) -> Dict[str, dict]:
        if self.__params is not None:
            return self.__params

        _params = {}
        for name, pd in self.raw_params.items():

            # flag
            # 参数未提供短标时，如果也未提供长标，则短标为 None，否则用长标填充短标
            # 短标为 None 时表明参数可能是一个位置参数
            if 'flag' not in pd or pd['flag'].strip() == '':
                if 'long_flag' not in pd or pd['long_flag'].strip() == '':
                    pd['flag'] = None
                else:
                    pd['flag'] = pd['long_flag']

            # type
            # 参数未提供类型时，参数类型为 str
            if 'type' not in pd:
                pd['type'] = 'str'

            pt = pd['type']
            if pt in ['str', 'string']:
                pd['type'] = 'str'

            elif pt in ['int', 'integer']:
                pd['type'] = 'int'

            # 布尔类型的参数必须提供短标或者长标，因为这个标志需要直接加入参数中
            elif pt in ['bool', 'boolean']:
                if pd['flag'] is None:
                    raise Exception(f'布尔类型的参数必须提供短标或者长标: {name}')
                pd['type'] = 'bool'

            elif pt == 'path':
                pass

            elif pt == 'ref':
                pd['default'] = self.env.get_path(pd['default'])

            elif pt in ('list', 'stdout', 'stderr'):
                pass

            else:
                raise Exception(f'Unit<{self.name}>: Unknown parameter type "{pd["type"]}"')

            # is_output
            # 参数表示输出路径，短标为空时通过重定向符 > 输出，否则通过参数标志输出
            if pd.get('is_output', False) and pd.get('flag') is None:
                raise Exception(f'output param must provide flag: {self.name}.{name}')

            _params[name] = pd

        self.__params = _params
        return _params

    @property
    def input_param_names(self) -> List[str]:
        return [x for x in self.param_names if self.params[x].get('is_input', False)]

    @property
    def input_param_name(self) -> str:
        if len(self.input_param_names) != 1:
            raise Exception(f'this method cannot be called for multi inputs unit: {self.name}')
        return self.input_param_names[0]

    @property
    def output_param_names(self) -> List[str]:
        arr = []
        for x in self.param_names:
            d = self.params[x]
            if d.get('is_output', False) or d.get('type') == 'stdout':
                arr.append(x)
        return arr

    @property
    def output_param_name(self) -> str:
        if len(self.output_param_names) != 1:
            raise Exception(f'this method cannot be called for multi outputs unit: {self.name} ({self.output_param_names})')
        return self.output_param_names[0]

    @property
    def path_param_names(self):
        """路径参数"""
        # d['type'] in ['stdout', 'stderr']
        arr = []
        for x in self.param_names:
            d = self.params[x]
            if d.get('is_output', False):
                arr.append(x)
            elif d['type'] in ['stdout', 'stderr']:
                arr.append(x)
            elif d['type'] == 'path':
                arr.append(x)
        return arr

    @staticmethod
    def create_from_file(unit_name: str, env: EnvLoader = None):
        """从指定的配置文件创建模块对象"""
        if exists(unit_name):
            name = filename(unit_name)
            configs = read_jsonlike_file(unit_name)

        else:
            assert env is not None, 'env cannot be none when unit_name as path not found'
            name = unit_name
            if name not in env.registered_module_units:
                raise f'unregistered unit: {name}'
            configs = read_jsonlike_file(env.registered_module_units[name])

        return Unit(name=name, configs=configs, env=env)
