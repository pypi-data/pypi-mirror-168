# coding=utf-8

import logging
import pickle
import shutil
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple

from exuse.extypings import SRecord, Mapping, Sequence, List, Union, Self
from exuse.expath import create_dir, join, exists, isfile, abspath, basename
from exuse.exio import read_jsonlike_file

from bioflowgraph.task import Task

from .env import EnvLoader
from .const import GRAPH_SAVING_TYPES, START_TASK, TASK_WAITING, TASK_SUCCESS, TASK_FAILED, APP_NAME


class BaseTaskGraph:
    """
    任务图模型：每个程序每执行一次为一个任务。
    一个程序在 n 个样本上执行 n 次生成 n 个任务。

    """
    __metaclass__ = ABCMeta

    def __init__(self, graph_name: str, output_dir: str, env: EnvLoader = None):
        self.graph_name = graph_name
        self.env = env
        self.output_dir = create_dir(output_dir)

        self.tasks: Mapping[str, Task] = {}
        self.START = Task('START')
        self.END = Task('END')

        # 模块单元的参数值，一般作为单元参数的默认值使用
        self.params: SRecord[dict] = {}
        self.templates: SRecord = {}

        self.ordered_tasks: Sequence[Task] = None
        self.dumped_pkl_file = join(self.output_dir, f'taskgraph.pkl')

    @abstractmethod
    def define_graph(self, sample_list_file: str):
        raise NotImplementedError('abstract metohd: define_graph')

    def _build_graph(self):
        """处理任务间的依赖，构建任务图"""
        # 处理任务节点之间的依赖
        for task_name, task in self.tasks.items():
            if len(task.dependencies) == 0:
                # 将没有依赖的任务挂载到 START 任务节点
                for ik in task.unit.input_param_names:
                    task.set_dep(self.START, f'{task.task_name}#{ik}', ik)

        # 如果一个任务不被任何任务依赖，将其添加到 END 节点的依赖中

    def _gen_commands(self):

        # sort tasks

        tasks: List[Task] = []

        def _iterate(ts: List[Task]):
            if len(ts) == 0:
                return
            next_ts = []
            for t in ts:
                tasks.append(t)
                for c in t.children:
                    next_ts.append(c)
            _iterate(next_ts)

        _iterate([self.START])

        order = {}
        for i, t in enumerate(tasks):
            if t.task_name in ['START', 'END']:
                continue
            order[t.task_name] = i
        tasks = [tasks[i] for i in order.values()]
        self.ordered_tasks = tasks

        for task in tasks:
            task.gen_command()

    def reset_task_status(self):
        "重置任务状态为 TASK_SUCCESS 或者 TASK_WAITING"
        self.START.status = TASK_SUCCESS
        for task in self.tasks.values():
            task.reset_status()

    def fetch_executable_tasks(self):
        "可执行任务：所有父任务 success 且自己 waiting"
        _executable_tasks: List[Task] = []

        def traverse(tasks: Sequence[Task]):
            # 没有子任务的任务会调用空列表
            if len(tasks) == 0:
                return

            next_tasks = []

            for task in tasks:
                # 索引任务时忽略输出节点
                if task.task_name == 'END':
                    continue
                # 可执行任务
                is_ready = True
                # 所有父任务都是 SUCCESS
                for t in task.parents:
                    if t.status != TASK_SUCCESS:
                        is_ready = False
                        break
                # 所有需要等待的任务也必须成功
                for tn in task.waits:
                    if self.tasks[tn].status != TASK_SUCCESS:
                        is_ready = False
                        break
                # 自己是 WAITING
                if is_ready and task.status != TASK_WAITING:
                    is_ready = False

                # 任务可执行时执行任务
                if is_ready:
                    if task not in _executable_tasks:
                        _executable_tasks.append(task)
                # 任务成功时依次检测其子任务
                elif task.status == TASK_SUCCESS:
                    for t in task.children:
                        next_tasks.append(t)

            traverse(next_tasks)

        self.START.status = TASK_SUCCESS
        traverse(self.START.children)
        return _executable_tasks

    def run(self, sample_list_file: str, params_file: str = None, **kwargs):
        if params_file is not None and isfile(params_file):
            self.params = read_jsonlike_file(params_file)
        self.define_graph(sample_list_file, **kwargs)
        self._build_graph()
        self._gen_commands()

    def create_unit_task(
        self,
        task_name: str,
        unit_name: str,
        dependencies: Mapping[str, Tuple[Self, str]] = None,
        params: SRecord = None,
        templates: SRecord = None,
        waits: Sequence[str] = None,
    ):

        if unit_name not in self.env.registered_module_units:
            raise Exception(f'未注册的模块单元 {unit_name}')

        if task_name in self.tasks:
            raise Exception(f'任务名重复 {task_name}')

        ## 用创建任务提供的参数值覆盖从单元配置文件中加载的默认参数值
        if params is None: params = {}
        task_params = {k: v for k, v in self.params.get(unit_name, {}).items()}  # deep copy
        task_params.update(params)

        self.tasks[task_name] = Task(
            task_name=task_name,
            unit_name=unit_name,
            working_dir=self.output_dir,
            dependencies=dependencies,
            params=task_params,
            templates=templates,
            waits=waits,
            env=self.env,
        )

        return self.tasks[task_name]

    def draw(
        self,
        add_ip=True,
        add_op=False,
        filename="taskgraph.gv",
        formats=None,
        node_styles=None,
    ):
        if formats is None:
            formats = GRAPH_SAVING_TYPES
        else:
            for fmt in formats:
                assert fmt in GRAPH_SAVING_TYPES, f'{fmt} not in {GRAPH_SAVING_TYPES}'
        if node_styles is None:
            node_styles = {}

        # apt install graphviz
        from graphviz import Digraph
        dot = Digraph(
            directory=self.output_dir,
            filename=filename,
            comment=f'Task Graph ({self.graph_name})',
        )

        for task_name in self.tasks:
            dot.node(task_name, **node_styles.get(task_name, {}))

        # edges from START
        if add_ip:
            dot.node('START', style='filled', color='.7 .3 1')
            for item in self.START.outputs:
                arr = item.split('.')
                dep = (('START', item), (arr[0], arr[1]))
                dot.edge(dep[0][0], dep[1][0])

        # 有效任务节点之间的边
        for task in self.tasks.values():
            for bd in task.dependencies:
                dot.edge(bd.sender.task_name, bd.receiver.task_name)

        # edges to END
        # if add_op:
        #     dot.node('END', shape='box', style='filled', color='.7 .3 1')
        #     for item in self.END.inputs:
        #         arr = item.split('.')
        #         dep = ((arr[0], arr[1]), ('END', item))
        #         # dot.edge(dep[0][0], dep[1][0], taillabel=dep[0][1])
        #         dot.edge(dep[0][0], dep[1][0])

        for fmt in formats:
            dot.render(format=fmt, view=False)

    # 按任务优先级打印任务 shell 命令
    def print_commands(self):
        if self.ordered_tasks is None:
            raise RuntimeError('run `TaskGraph::run()` first!')
        for task in self.ordered_tasks:
            print(f'\033[1;36m{task.task_name} 🍍\033[0m {task.main_shell_cmd}')

    @classmethod
    def load(cls: Self, pickle_path: str) -> Self:
        with open(pickle_path, 'rb') as rb:
            return pickle.load(rb)

    @classmethod
    def create(
        cls: Self,
        name: str,
        sl_fp: str,
        working_dir: str = None,
        env_file: str = None,
        params_file: str = None,
        draw=True,
        override=False,
        **kwargs,
    ) -> Self:
        assert exists(sl_fp), f'sample list file must be provided!'

        env = None
        if env_file is None:
            if exists('env.toml'):
                env_file = 'env.toml'
                logging.info(f'auto use env {abspath(env_file)}')
            else:
                logging.info(f'not use any env file!')
        if env_file is not None:
            env = EnvLoader(env_file, strict=True, checking_path=False)

        if working_dir is None:
            working_dir = create_dir(EnvLoader.graph_working_dir)

        graph_dir = join(working_dir, name)
        if exists(graph_dir) and override:
            shutil.rmtree(graph_dir)
        logging.info(f'graph will work in {graph_dir}')

        graph: Self = cls(name, output_dir=graph_dir, env=env)
        graph.run(sl_fp, params_file=params_file, **kwargs)
        if draw:
            graph.draw()

        return graph


class TaskGraph(BaseTaskGraph):

    def add_fq(self, name: str, files: Sequence[str]):
        """Add fq files to the root task and return the root task"""
        if name in self.START.params:
            raise KeyError(f'{name} has been mounted!')
        self.START.params[name] = files
        return self.START

    def add_bwa(self, sname: str, fq1s: Sequence[str], fq2s: Sequence[str]):
        """run possible cat, run bwa and return the bwa task"""
        fq1_name = f'{sname}_fq1'
        fq2_name = f'{sname}_fq2'
        start = self.add_fq(fq1_name, fq1s)
        start = self.add_fq(fq2_name, fq2s)

        deps = {}

        if len(fq1s) == 1:
            deps['fq_1'] = (start, fq1_name)
        else:
            _d = {'targets': (start, fq1_name)}
            cat = self.add_task(fq1_name, 'cat', _d, {'dest': f'{fq1_name}.fq.gz'})
            deps['fq_1'] = (cat, 'dest')

        if len(fq2s) == 1:
            deps['fq_2'] = (start, fq2_name)
        else:
            _d = {'targets': (start, fq2_name)}
            cat = self.add_task(fq2_name, 'cat', _d, {'dest': f'{fq2_name}.fq.gz'})
            deps['fq_2'] = (cat, 'dest')

        return self.add_task(sname, 'bwamem2', deps)

    def add_task(
        self,
        sample_name: str,
        unit_name: str,
        dependencies: Mapping[str, Tuple[Self, str]] = None,
        templates: SRecord = None,
        params: SRecord = None,
    ):
        """为一个样本添加一个任务"""
        if params is None: params = {}
        if templates is None: templates = {}
        task_name = f'{unit_name}-{sample_name}'

        templates['SampleID'] = templates.get('SampleID', sample_name)
        templates['SampleName'] = templates.get('SampleName', sample_name)

        return self.create_unit_task(
            unit_name=unit_name,
            task_name=task_name,
            dependencies=dependencies,
            params=params,
            templates=templates,
        )
