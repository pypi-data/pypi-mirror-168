# coding=utf-8

from collections import defaultdict
from inspect import isfunction
import re
from typing import Generic, TypeVar
import psutil
import logging
import subprocess
from exuse.expath import join, exists, abspath, isabs, dirname, makedirs, create_dir
from exuse.extypings import Mapping, Sequence, Tuple, Self, List, SSRecord, SRecord
from exuse import exio

from .const import SHELL_DIR, STDXXX_DIR, TASK_WAITING, TASK_RUNNING, TASK_SUCCESS, TASK_FAILED, SUCCESS_DIR
from .env import EnvLoader
from .unit import Unit


def joinfv(f=None, v=None):
    return ''.join([
        '' if f is None else f'{f}',
        ' ' if f is not None and v is not None else '',
        '' if v is None else f'{v}',
    ])


T = TypeVar('T')


class Binding(Generic[T]):

    def __init__(self, sender: T, send: str, receiver: T, receive: str, fmt=None):
        self.sender = sender
        self.send = send
        self.receiver = receiver
        self.receive = receive
        self.fmt = fmt

    def __str__(self) -> str:
        return f'Binding[{self.sender} {self.send} => {self.receiver} {self.receive}]'


class Task:
    """one task, one running on a unit!"""

    def __init__(
        self: Self,
        task_name: str,
        unit_name: str = None,
        working_dir: str = None,
        # 该任务执行需要等待依赖的所有任务执行成功 (dep_task, sender=None, receiver=None, replacer=None)
        dependencies: Mapping[str, Tuple[Self, str]] = None,
        # TODO 等待指定任务执行完成，但是与之没有依赖关系
        waits: Sequence[str] = None,
        params: SRecord = None,
        templates: SRecord = None,
        env: EnvLoader = None,
    ):
        # 任务图中的任务名称是唯一的
        self.task_name: str = task_name
        # 任务绑定的执行单元名称
        self.unit_name: str = unit_name
        # 任务绑定的执行单元
        self.unit: Unit = None
        # 任务的实时运行状态，默认为等待运行
        self.status: int = TASK_WAITING
        # 任务正在使用的或者使用过的进行号
        self.pid = None
        # 重载任务时的状态，用于绘图; 因为重载时失败的任务会被修改为等待，才能置入队列开始运行, 所以需要一个单独的变量记录
        self.vis_status: int = TASK_WAITING
        # 任务运行的生信环境
        self.env: EnvLoader = env
        # 任务子目录的保存位置，在任务图中运行时该路径指向任务图的输出目录
        self.working_dir: str = working_dir

        # 任务的依赖任务，格式为 {self_input_key: (DepTask, dep_output_key, tpl)}
        # tpl 是一个字符串，可以对 DepTask.dep_output_key 的路径进行校正
        # 可以用 {} 表示依赖任务输出路径的 basename
        # 适用于依赖任务的 output_key 是一个目录，而下游任务只依赖于目录下的一个文件的情况
        self.dependencies: List[Binding[Self]] = []
        self.__registered_deps = []

        # 任务的运行时参数，键是参数名称，值是参数值
        self.params: SRecord = {} if params is None else params

        # 拼接命令时对参数值中的模板变量进行替换，模板变量用 ${} 表示
        # TODO 模板变量统一修改成 {} 形式
        tpls = {} if templates is None else templates
        tpls['TaskName'] = self.task_name
        tpls['WorkingDir'] = self.working_dir
        self.templates = tpls

        # 与依赖类似，等待也是一种依赖关系，但是它与父任务间没有 IO 交换
        # TODO 合并到依赖中，DepTask 表示等待，(DepTask, output_key) 表示依赖
        self.waits = [] if waits is None else waits

        # 直接依赖本任务的子任务列表
        self.children: List[Self] = []
        # 本人无直接依赖的任务列表
        self.parents: List[Self] = []

        # 当前节点与其父节点和子节点的连接关系
        # { parent_unit.some_output => this_unit.some_input }
        self.inputs: SSRecord = {}
        # { this_unit.some_output => child_unit.some_input }
        self.outputs: SSRecord = {}

        self.output_dir: str = None  # 任务输出目录
        self.shell_dir: str = None  # 保存命令
        self.stdxxx_dir: str = None  # 保存输出和错误

        self.shell_cmd: str = None  # 任务完整的命令
        self.shell_cmd_main: str = None  # 任务命令的主干部分
        self.shell_file: str = None  # 保存完整命令的文件
        self.success_flag_file: str = None  # 任务成功时需要创建的标志文件

        # 当前节点与其父节点和子节点的连接关系
        # { parent_unit.some_output => this_unit.some_input }
        self.inputs: SSRecord = {}
        # { this_unit.some_output => child_unit.some_input }
        self.outputs: SSRecord = {}

        if unit_name is not None:
            unit = self._init_unit()

            if dependencies is not None:
                _deps = {}
                if isinstance(dependencies, Task):
                    _deps[unit.input_param_name] = (dependencies, dependencies.unit.output_param_name)
                elif isinstance(dependencies, tuple):
                    _deps[unit.input_param_name] = dependencies
                elif isinstance(dependencies, dict):
                    for k, d in dependencies.items():
                        if isinstance(d, Task):
                            _deps[k] = (d, d.unit.output_param_name)
                        else:
                            _deps[k] = d

                for receive, d in _deps.items():
                    self.set_dep(d[0], d[1], receive)

    def set_dep(self, sender: Self, send: str = None, receive: str = None, fmt: str = None):
        """创建新的依赖
        
        Args:
            dep_task: 依赖的任务
            sender: 依赖任务的输出端
            receiver: 本任务的输入端
            replacer: 用输出替换输入时进行一定的处理
        """

        k = f'{sender}.{send}=>{self}.{receive}'
        if k in self.__registered_deps:
            raise Exception(f'{sender}.{sender} has already append to the dependencies of {self}.{receive}')

        # 和依赖任务间不存在文件交换
        if send is None or receive is None:
            self.dependencies.append(Binding(sender, None, self, None))
        else:
            self.dependencies.append(Binding(sender, send, self, receive, fmt))

        if sender not in self.parents:
            self.parents.append(sender)

        if self not in sender.children:
            sender.children.append(self)

    def gen_command(self, save=True):
        """可以提供参数值覆盖初始化时提供的默认参数"""
        unit = self.unit

        ## 先填充输入参数值, 可能是数组
        receive_mappings = defaultdict(list)
        for bd in self.dependencies:
            values = bd.sender.params[bd.send]
            if isinstance(values, str):
                values = [values]

            for v in values:
                if bd.fmt is not None:
                    v = bd.fmt(v)
                receive_mappings[bd.receive].append(v)

        for receive, arr in receive_mappings.items():
            self.params[receive] = arr

        ## 再检查必须参数
        for k, d in self.unit.params.items():
            is_required = d.get('required', False)
            if is_required and k not in self.params:
                raise Exception(f'{self}: parameter "{k}" is required!')

        ## 调整输出路径的位置
        for k in self.unit.path_param_names:
            if k not in self.params or self.params[k] is None:
                raise Exception(f'{self}: output parameter "{k}" is not provided!')

            p = self.params[k]

            # 输出路径是一些特殊值
            if p[0] in ['#', '/'] or isabs(p):
                self.params[k] = p
                # stderr 重定向到 stdout
            elif p in ('&1', 'stderr', 'STDERR'):
                self.params[k] = p
            else:
                self.params[k] = abspath(join(self.output_dir, p))

        # executor & subexecutor
        cmds = [unit.executor]
        if unit.sub_executor is not None:
            cmds.append(unit.sub_executor)

        consumed_params = []
        for pn in unit.param_names:
            pv = self.params.get(pn)
            if pv is None: continue
            if isinstance(pv, list):
                pv = ' '.join(pv)
            ############################
            consumed_params.append(pn)
            pd = unit.params[pn]
            pt, pf = pd['type'], pd['flag']

            cmd = None
            if pt == 'bool':
                if pv is True:
                    cmd = joinfv(pf, None)
            elif pt == 'int' or pt == 'float':
                cmd = joinfv(pf, pv)
            elif pt == 'list':
                # TODO 需要区分两种列表参数类型
                cmd = joinfv(pf, pv)
            else:
                _pv = self.replace_tpl(pv)
                if pt == 'stdout':
                    cmd = '>' + _pv
                elif pt == 'stderr':
                    cmd = '2>' + _pv
                else:
                    cmd = joinfv(pf, _pv)
                self.params[pn] = _pv
            cmds.append(cmd)

        undo_params = [p for p in self.params.keys() if p not in consumed_params]
        if len(undo_params) > 0:
            logging.info(f'Parameters not consumed: {", ".join(undo_params)}')

        cmd = ' '.join(cmds)

        # 命令执行完成之后创建一个 .TASK_DONE 文件表示任务成功
        self.main_shell_cmd = cmd
        cmd = f"({cmd}) && (touch {self.success_flag_file})"

        self.shell_cmd = cmd

        if save:
            if exists(self.shell_file):
                raw_shell = exio.read_file(self.shell_file)
                if cmd != raw_shell:
                    logging.warning(f'override {self} shell: {self.shell_file}')
                    exio.write(cmd, self.shell_file)
            else:
                exio.write(cmd, self.shell_file)

        return cmd

    @property
    def desc(self):
        name = self.task_name
        d_a = [d[0].task_name for d in self.dependencies.values()]
        d_s = '' if len(d_a) == 0 else ', deps=[' + ', '.join(d_a) + ']'
        w_s = '' if len(self.waits) == 0 else ', waits=[' + ', '.join(self.waits) + ']'
        p_a = [o.task_name for o in self.parents if o.task_name != 'START']
        p_s = '' if len(p_a) == 0 else ', parents=[' + ', '.join(p_a) + ']'
        c_a = [o.task_name for o in self.children if o.task_name != 'END']
        c_s = '' if len(c_a) == 0 else ', children=[' + ', '.join(c_a) + ']'
        return f'Task<{name}{p_s}{w_s}{c_s}{d_s}>'

    @property
    def stdout_file(self):
        return self.replace_tpl(self.params[self.unit.stdout_key])

    @property
    def stderr_file(self):
        return self.replace_tpl(self.params[self.unit.stderr_key])

    def __eq__(self, other: Self) -> bool:
        return self.task_name == other.task_name

    def __str__(self) -> str:
        # return f'task \033[1;31m{self.task_name}\033[0m'
        return f'\033[1;31m{self.task_name}\033[0m'

    def replace_tpl(self, s: str):
        """替换字符串中的模板变量"""
        for tpl in re.findall(r'\$\{.*?\}', s):
            tpl_var = tpl[2:-1]
            if tpl_var not in self.templates:
                msg = f'No template value provided for "{tpl_var}" for {self}'
                raise Exception(msg)
            s_or_f = self.templates[tpl_var]
            if isfunction(s_or_f):
                s = s_or_f(s)
            else:
                s = s.replace(tpl, s_or_f)
        return s

    def reset_status(self):
        """重置任务状态为 TASK_SUCCESS 或者 TASK_WAITING"""
        if exists(self.success_flag_file):
            self.status = TASK_SUCCESS
        else:
            self.status = TASK_WAITING

    def refresh_status(self):
        """
        刷新任务状态。
        成功和失败的任务不再刷新。
        生成 success 文件将任务置为成功。

        """
        if self.status in (TASK_SUCCESS, TASK_FAILED):
            return

        # 生成 success 文件表示任务成功
        if exists(self.success_flag_file):
            self.status = TASK_SUCCESS

        # 没有分配进程号表示等待中
        elif self.pid is None:
            self.status = TASK_WAITING

        else:
            try:
                proc = psutil.Process(self.pid)
                self.status = TASK_RUNNING
                if proc.status() == 'zombie':
                    proc.wait()
            # 任务拥有进程号，但是该进程没有在运行，同时也没有生成 success 文件，判定为失败
            except psutil.NoSuchProcess:
                self.status = TASK_FAILED

        self.vis_status = self.status

    def start(self):
        if self.shell_cmd is not None:
            flag_dir = dirname(self.success_flag_file)
            if not exists(flag_dir):
                makedirs(flag_dir)
            proc = subprocess.Popen(self.shell_cmd, shell=True, stdout=subprocess.PIPE)
            self.pid = proc.pid
            self.status = TASK_RUNNING
        else:
            raise Exception(f'No command generated for {self.task_name}')

    def update_params(self, params: SRecord, solve_conflict="ignore"):
        """更新任务参数值"""
        assert solve_conflict in ['ignore', 'override']
        for k, v in params.items():
            if k in self.params:
                if solve_conflict == 'override':
                    self.params[k] = v
            else:
                self.params[k] = v

    # 如果提供了执行单元，执行执行单元的初始化设置
    def _init_unit(self):
        self.output_dir = create_dir(self.working_dir, self.unit_name)
        self.shell_dir = create_dir(self.output_dir, SHELL_DIR)
        self.stdxxx_dir = create_dir(self.output_dir, STDXXX_DIR)
        self.shell_file = join(self.shell_dir, f'{self.task_name}.sh')
        self.success_flag_file = join(create_dir(self.output_dir, SUCCESS_DIR), self.task_name)
        self.templates['UnitName'] = self.unit_name
        self.templates['OutputDir'] = self.output_dir
        self.templates['ShellDir'] = self.shell_dir
        self.templates['StdxxxDir'] = self.stdxxx_dir

        self.unit = Unit.create_from_file(self.unit_name, self.env)

        # 任务初始化时没有提供值的参数使用单元文件提供的默认值
        for k, d in self.unit.params.items():
            if 'default' in d:
                self.params[k] = self.params.get(k, d['default'])

        return self.unit