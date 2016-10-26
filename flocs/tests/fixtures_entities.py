"""Entities objects for testing purposes
"""
from flocs.entities import Task, TaskSession, Student


ENTITIES = {
    'ts1': TaskSession(
        task_session_id=81,
        student_id=13,
        task_id=28,
        solved=False,
        given_up=False,
    ),
    'ts2': TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        solved=False,
        given_up=False,
    ),
    'ts2s': TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        solved=True,
        given_up=False,
    ),
    'ts2g': TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        solved=False,
        given_up=True,
    ),
    'ts3': TaskSession(
        task_session_id=27,
        student_id=37,
        task_id=28,
        solved=False,
        given_up=False,
    ),
    't1': Task(
        task_id=28,
        setting=None,
        solution=None,
    ),
    't2': Task(
        task_id=67,
        setting=None,
        solution=None,
    ),
    't3': Task(
        task_id=55,
        setting=None,
        solution=None,
    ),
    'stud1': Student(
        student_id=13,
        last_task_session=81
    ),
    'stud2': Student(
        student_id=37,
        last_task_session=14
    ),
}


def task_sessions_dict(*keys):
    return {ENTITIES[key].task_session_id: ENTITIES[key] for key in keys}


def tasks_dict(*keys):
    return {ENTITIES[key].task_id: ENTITIES[key] for key in keys}


def students_dict(*keys):
    return {ENTITIES[key].student_id: ENTITIES[key] for key in keys}
