# coding=utf-8

APP_NAME = 'bioflowgraph'

PROC_RUNNING = "running"
PROC_SLEEPING = "sleeping"
PROC_DISK_SLEEP = "disk-sleep"
PROC_STOPPED = "stopped"
PROC_TRACING_STOP = "tracing-stop"
PROC_ZOMBIE = "zombie"
PROC_DEAD = "dead"
PROC_WAKE_KILL = "wake-kill"
PROC_WAKING = "waking"
PROC_IDLE = "idle"  # Linux, macOS, FreeBSD
PROC_LOCKED = "locked"  # FreeBSD
PROC_WAITING = "waiting"  # FreeBSD
PROC_SUSPENDED = "suspended"  # NetBSD
PROC_PARKED = "parked"  # Linux

TASK_WAITING = 0
TASK_RUNNING = 1
TASK_SUCCESS = 2
TASK_FAILED = 3

TRANS_TASK = {0: 'waiting', 1: 'running', 2: 'successful', 3: 'failed'}
TRANS_TASK_T = {k: v for v, k in TRANS_TASK.items()}

SUCCESS_DIR = '_success'  # 存放 success 标志文件
SHELL_DIR = '_shell'  # 存放 shell 脚本
STDXXX_DIR = '_shell'  # 存放 stdout 和 stderr 文件

START_TASK = 'START'
END_TASK = 'END'

GRAPH_SAVING_TYPES = ('pdf', 'svg', 'png')

NODE_FILL_COLORS = {0: 'white', 1: '#99cc66', 2: '#0099cc', 3: '#ff0033'}
