""" Domain data
"""
from .entities import Task

TASKS = (
    Task(task_id=0, ref='three-steps-forward'),
    Task(task_id=1, ref='diamond-on-right'),
    Task(task_id=2, ref='zig-zag'),
)


def create_tasks_dict():
    return {task.task_id: task for task in TASKS}
