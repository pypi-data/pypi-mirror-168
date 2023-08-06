# coding=utf-8

import time
import logging
from queue import Queue
from os.path import join, exists, basename
from typing import List
from typing_extensions import Self
from collections import defaultdict
from exuse.exio import dump_json, load_json

from .const import NODE_FILL_COLORS, TASK_WAITING, TASK_RUNNING, TASK_SUCCESS, TASK_FAILED, TRANS_TASK, TRANS_TASK_T
from .task_graph import TaskGraph
from .task import Task


class TaskPolling:
    """任务轮询对象，调用 run() 执行任务图。"""

    def __init__(self, tg: TaskGraph, maxsize=1, interval=5):
        self.tg = tg
        self.maxsize = maxsize  # 任务队列容量
        self.interval = interval  # 队列刷新周期
        self.running_queue = Queue(maxsize)
        self.task_status_file = join(self.output_dir, 'status.json')
        self.task_pid_file = join(self.output_dir, 'pid.json')
        self.meta_file = join(self.output_dir, 'meta.json')
        self.vis_status_file = join(self.output_dir, 'taskgraph.status.gv')

        # self.tg.reset_task_status()
        self.num_executable_tasks = None

        self.restore()

    @property
    def output_dir(self):
        return self.tg.output_dir

    @property
    def tasks(self):
        return self.tg.tasks

    def is_empty_queue(self):
        return self.running_queue.empty()

    def is_full_queue(self):
        return self.running_queue.full()

    def run(self):
        meta = {'graph_name': self.tg.graph_name}
        dump_json(meta, self.meta_file, 2)

        while True:
            self.refresh_queue()
            self.save_infos()
            # 任务图中没有可执行任务：全部成功，或者部分失败阻塞后续执行
            # 队列为空时，所有可执行任务执行完毕
            if self.num_executable_tasks == 0 and self.is_empty_queue():
                self.stat_tasks()
                self.draw_with_status()
                logging.info('no executable task now, exit')
                break
            self.stat_tasks()
            self.draw_with_status()
            time.sleep(self.interval)

    def refresh_queue(self) -> List[Task]:
        new_tasks = []
        _ = 'Check running tasks'
        if self.is_empty_queue():
            logging.debug(f"{_}: no task is running")
        else:
            logging.debug(_)
            self.refresh_tasks()

        _ = 'Update running queue'
        if self.is_full_queue():
            logging.debug(f'{_}: queue is already full')
        else:
            logging.debug(_)
            executable_tasks = self.tg.fetch_executable_tasks()
            self.num_executable_tasks = len(executable_tasks)
            for task in executable_tasks:
                if self.is_full_queue():
                    break
                logging.info(f'{task} starts ...')
                self.running_queue.put(task)
                task.start()
                new_tasks.append(task)
        return new_tasks

    def refresh_tasks(self):
        """刷新当前任务队列中所有任务的状态"""
        counter = 0
        while (counter < self.maxsize):
            counter += 1
            if self.is_empty_queue():
                break
            task: Task = self.running_queue.get()
            task.refresh_status()
            if task.status == TASK_RUNNING:
                self.running_queue.put_nowait(task)
            elif task.status == TASK_FAILED:
                logging.info(f"{task} is \033[1;37;43mfailed\033[0m! See {task.stderr_file}")
            else:
                logging.info(f"{task} is \033[1;34msuccessful\033[0m!")

    def stat_tasks(self):
        d = defaultdict(int)
        for task in self.tg.tasks.values():
            d[task.status] += 1
        # _ = CoStr.get("{} running, {} successful and {} failed", 'yellow')
        _ = "{} running, {} successful and {} failed"
        logging.info(_.format(d[TASK_RUNNING], d[TASK_SUCCESS], d[TASK_FAILED]))

    def save_infos(self):
        status = {}
        pid = {}
        for task in self.tg.tasks.values():
            status[task.task_name] = TRANS_TASK[task.status]
            if task.pid is not None:
                pid[task.task_name] = task.pid
        dump_json(status, self.task_status_file, 2)
        dump_json(pid, self.task_pid_file, 2)

    def restore(self):
        if not exists(self.task_status_file): return
        logging.info(f'\033[1;33mrestore task graph from {self.task_status_file}\033[0m')
        # restore task pids
        # 只有上次处于运行中的任务会设置PID
        #for k, v in load_json(self.task_pid_file).items():
        #    if self.tasks[k].status == TASK_RUNNING:
        #        self.tasks[k].pid = v

        # restore task status
        for k, v in load_json(self.task_status_file).items():
            status = int(TRANS_TASK_T.get(v, v))
            self.tasks[k].vis_status = status
            # 上次运行失败的任务，本次重新运行
            if status in (TASK_FAILED, TASK_RUNNING):
                self.tasks[k].status = TASK_WAITING
            else:
                self.tasks[k].status = status
                # 正在运行中的任务还需要推入任务队列
                # if status == TASK_RUNNING:
                #    self.running_queue.put(self.tasks[k])

    def draw_with_status(self):
        node_styles = {}
        for task_name, task in self.tasks.items():
            node_styles[task_name] = {
                'style': 'filled',
                'fillcolor': NODE_FILL_COLORS[task.vis_status],
            }
        self.tg.draw(filename=basename(self.vis_status_file), formats=['png'], node_styles=node_styles)

    @classmethod
    def from_tg_pkl(cls, fp: str, **kwargs) -> Self:
        """从保存的 TaskGraph 对象中创建 TaskPolling 对象"""
        tg = TaskGraph.load(fp)
        tp = cls(tg, **kwargs)
        return tp

    @classmethod
    def from_tg_dir(cls, dp: str, **kwargs) -> Self:
        tg_fp = join(dp, 'taskgraph.pkl')
        assert exists(tg_fp)
        tp = cls.from_tg_pkl(tg_fp, **kwargs)
        return tp
