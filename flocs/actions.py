"""
Module defining all possible action types and providing action creators
"""
from collections import namedtuple
from datetime import datetime
from enum import Enum


StartTaskInstance = namedtuple('StartTaskInstance', [
    'student_id',
    'task_id',
    #'task_instance_id',
    #'time',
])


SolveTaskInstance = namedtuple('SolveTaskInstance', [
    'task_instance_id',
    #'time',
])


GiveUpTaskInstance = namedtuple('GiveUpTaskInstance', [
    'task_instance_id',
    #'time',
])


## additional action creators

def create_start_task_instance(student_id, task_id):
    # TODO: should first emit create_task_instance action? (as a prerequisite)
    task_instance_id = 0  # TODO: compute next unique id (how to solve race condition problem???)
    time = datetime.now()
    return StartTaskInstance(student_id, task_id, task_instance_id, time)



