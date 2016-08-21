""" Type definitions for domain entities
"""
from collections import namedtuple


Student = namedtuple('Student', [
    'student_id',
    ])


Task = namedtuple('Task', [
    'task_id',
    'ref',
    ])


TaskInstance = namedtuple('TaskInstance', [
    'task_instance_id',
    'student_id',
    'task_id',
    'solved',
    'given_up',
    ])


TaskStats = namedtuple('TaskStats', [
    'task_id',
    'started_count',
    'solved_count',
    'given_up_count',
    ])
