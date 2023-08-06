# coding=utf-8

import os
import re
from typing import Any, TypeVar, Union
import psutil
import logging
import subprocess
from exuse.expath import join, exists, abspath, isabs, dirname, makedirs, create_dir
from exuse.extypings import Mapping, Sequence, Tuple, Self, List, SSRecord, SRecord
from exuse import exio

from .const import SHELL_DIR, START_TASK, STDXXX_DIR, TASK_WAITING, TASK_RUNNING, TASK_SUCCESS, TASK_FAILED, SUCCESS_DIR
from .env import EnvLoader
from .unit import Unit

# Task: 当前任务的唯一输入依赖于指定任务的唯一输出
# Mapping[str, Task]：当期任务的某个输入依赖于指定任务的唯一输出
# Mapping[str, tuple[Task, str]]：当前任务的某个输出依赖于指定任务的某个输出
T = TypeVar('T')
DepType = Mapping[str, tuple[T, str]]
DepType0 = Union[T, str, Tuple[T, str], Mapping[str, T], Mapping[str, str], DepType]


def joinfv(f=None, v=None):
    return ''.join([
        '' if f is None else f'{f}',
        ' ' if f is not None and v is not None else '',
        '' if v is None else f'{v}',
    ])


class Task:
    """one task, one running on a unit!"""

    def __init__(
        self: Self,
        task_name: str,
        unit_name: str = None,
        working_dir: str = None,
        # 该任务执行需要等待依赖的所有任务执行成功
        dependencies: DepType0[Self] = None,
        # TODO 等待指定任务执行完成，但是与之没有依赖关系
        waits: Sequence[str] = None,
        params: SRecord = None,
        templates: SRecord = None,
        env: EnvLoader = None,
    ):
        self.task_name = task_name
        self.status = TASK_WAITING
        self.vis_status = TASK_WAITING  # 用于绘图的状态
        self.env = env

        self.unit_name = unit_name
        self.dependencies: DepType[Self] = {}
        self.params = {} if params is None else params
        self.templates = {} if templates is None else templates
        self.waits = [] if waits is None else waits

        self.unit: Unit = None
        self.children: List[Self] = []
        self.parents: List[Self] = []
        # 当前节点与其父节点和子节点的连接关系
        # { parent_unit.some_output => this_unit.some_input }
        self.inputs: SSRecord = {}
        # { this_unit.some_output => child_unit.some_input }
        self.outputs: SSRecord = {}
        # 任务运行状态

        if unit_name is None:
            # 无单元任务：输入啥，就输出啥
            pass
        else:
            self.output_dir = create_dir(working_dir, unit_name)
            self.shell_dir = create_dir(self.output_dir, SHELL_DIR)
            self.stdxxx_dir = create_dir(self.output_dir, STDXXX_DIR)
            self.shell_file = join(self.shell_dir, f'{task_name}.sh')
            self.shell_cmd: str = None
            self.main_shell_cmd: str = None
            self.success_flag_file = join(create_dir(self.output_dir, SUCCESS_DIR), task_name)
            self.pid = None  # 任务正在使用的或者使用过的进行号

            default_templates = {
                'TaskName': task_name,
                'UnitName': unit_name,
                'WorkingDir': working_dir,
                'OutputDir': self.output_dir,
                'ShellDir': self.shell_dir,
                'StdxxxDir': self.stdxxx_dir
            }
            for k, v in default_templates.items():
                if k not in self.templates:
                    self.templates[k] = v

            self._set_unit()
            if dependencies is not None:
                self.set_dependencies(dependencies)

    @classmethod
    def create_empty_task(cls):
        pass

    def _set_unit(self):
        assert self.env is not None, 'env must be provided when init unit'
        unit = Unit.create_from_file(unit_name=self.unit_name, env=self.env)

        for k, d in unit.params.items():
            # 任务初始化时没有提供值的参数使用单元文件提供的默认值
            if 'default' in d:
                self.params[k] = self.params.get(k, d['default'])

        # 检查必须参数的值
        # for k, d in unit.raw_params.items():
        #     if d.get('required', False) and k not in self.params:
        #         raise Exception(f'{self}: parameter "{k}" is required!')

        # 修改任务的路径参数值的路径到工作目录下
        for k in unit.path_param_names:
            if k not in self.params:
                raise Exception(f'{self}: output parameter "{k}" is not provided!')

            p = self.params[k]
            if p[0] in ['#', '/'] or isabs(p):
                np = p
            else:
                np = abspath(join(self.output_dir, p))
            self.params[k] = np

        self.unit = unit

    def set_dependencies(self, deps: DepType0[Self]):
        """
        定义一个依赖：
        # - `str` 直接为当前任务的唯一输入指定值
        - `Task` 当前任务的唯一输入依赖于指定任务的唯一输出，或者与当前任务唯一输入同名的输出
        - `(Task, str)` 当期任务的唯一输入依赖于指定任务的指定输出
        # - `{str: str}` 直接为当前任务的某个输入指定值
        - `{str: Task}` 当前任务的指定输入依赖于指定任务的唯一输出，或者与指定输入同名的输出
        - `{str: (Task, str)}` 的指定输入依赖于指定任务的指定输出
        """
        _deps = {}
        if not isinstance(deps, dict):
            _deps[self.unit.input_param_name] = deps
        else:
            _deps = {k: d for k, d in deps.items()}

        std_deps: DepType[Self] = {}
        for k, d in _deps.items():
            e = f'invalid dependency declare for {self} => {k}'
            if k not in self.unit.input_param_names:
                raise KeyError(f'{k} is not input of {self.unit.name}')

            # 依赖于指定任务的唯一输出，或者与当前任务唯一输入同名的输出
            if isinstance(d, Task):
                if len(d.unit.output_param_names) == 1:
                    std_deps[k] = (d, d.unit.output_param_name)
                else:
                    assert k in d.unit.output_param_names, e
                    std_deps[k] = (d, k)
            else:
                # START or else task
                dep_task: Task = d[0]
                assert isinstance(dep_task, Task), e
                # assert d[1] in dep_task.unit.output_param_names, e
                if dep_task.task_name == START_TASK:
                    nk = f'{self.task_name}.{k}'
                    dep_task._update_links(dep_task, self, {nk: k})
                    dep_task.params[nk] = d[1]
                    std_deps[k] = (d[0], nk)
                else:
                    std_deps[k] = d

        self.dependencies = std_deps

    def __eq__(self, other: Self) -> bool:
        return self.task_name == other.task_name

    def __str__(self) -> str:
        # return f'task \033[1;31m{self.task_name}\033[0m'
        return f'\033[1;31m{self.task_name}\033[0m'

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

    def _update_links(self, start_task: Self, end_task: Self, links: Mapping[str, str]):
        for start, end in links.items():
            if start not in start_task.outputs:
                start_task.outputs[start] = (end_task.task_name, end)
            if end not in end_task.inputs:
                end_task.inputs[end] = (start_task.task_name, start)

    def get_parent(self, name: str):
        for task in self.parents:
            if task.task_name == name:
                return task
        return None

    def add_parent(self, parent: Self, links: Mapping[str, str]):
        if parent not in self.parents:
            self.parents.append(parent)
            self._update_links(parent, self, links)
            parent.add_child(self, links)

    def add_child(self, child: Self, links: Mapping[str, str]):
        if child not in self.children:
            self.children.append(child)
            self._update_links(self, child, links)
            child.add_parent(self, links)

    def gen_command(self, save=True):
        """可以提供参数值覆盖初始化时提供的默认参数"""
        # 任务没有依赖时它可能是

        # 从父任务的输出参数中更新本任务的输入参数
        # print(self.task_name, 666, self.dependencies)
        for k, d in self.dependencies.items():
            dep_task: Self = d[0]
            # print(self.task_name, k, d)
            if dep_task.task_name == START_TASK:
                self.params[k] = d[1]
            else:
                self.params[k] = dep_task.params[d[1]]

        unit = self.unit

        # executor & subexecutor
        cmds = [unit.executor]
        if unit.sub_executor is not None:
            cmds.append(unit.sub_executor)

        consumed_params = []
        for pn in unit.param_names:
            pv = self.params.get(pn)
            if pv is None:
                continue
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
                cmd = joinfv(pf, ' '.join([str(i) for i in pv]))
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

    def replace_tpl(self, cmd: str):
        for tpl in re.findall(r'\$\{.*?\}', cmd):
            tpl_var = tpl[2:-1]
            if tpl_var not in self.templates:
                msg = f'No template value provided for "{tpl_var}" when making cmd `{cmd}` for unit "{self.task_name}"'
                raise Exception(msg)
            cmd = cmd.replace(tpl, str(self.templates[tpl_var]))
        return cmd

    def update_params(self, params: SRecord, solve_conflict="ignore"):
        """更新任务参数值"""
        assert solve_conflict in ['ignore', 'override']
        for k, v in params.items():
            if k in self.params:
                if solve_conflict == 'override':
                    self.params[k] = v
            else:
                self.params[k] = v

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

    def feed(self, data: Mapping[str, Any]):
        # 统统接受，方便无单元任务传递参数
        for k, v in data.items():
            self.params[k] = v
