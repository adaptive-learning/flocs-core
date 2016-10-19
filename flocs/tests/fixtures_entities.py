"""Entities objects for testing purposes
"""
from flocs.entities import Task, TaskInstance, Student


ENTITIES = {
    'ti1': TaskInstance(
        task_instance_id=81,
        student_id=13,
        task_id=28,
        solved=False,
        given_up=False,
    ),
    'ti2': TaskInstance(
        task_instance_id=14,
        student_id=37,
        task_id=67,
        solved=False,
        given_up=False,
    ),
    'ti2s': TaskInstance(
        task_instance_id=14,
        student_id=37,
        task_id=67,
        solved=True,
        given_up=False,
    ),
    'ti2g': TaskInstance(
        task_instance_id=14,
        student_id=37,
        task_id=67,
        solved=False,
        given_up=True,
    ),
    'ti3': TaskInstance(
        task_instance_id=27,
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
        last_task_instance=81
    ),
    'stud2': Student(
        student_id=37,
        last_task_instance=14
    ),
}


def task_instances_dict(*keys):
    return {ENTITIES[key].task_instance_id: ENTITIES[key] for key in keys}


def tasks_dict(*keys):
    return {ENTITIES[key].task_id: ENTITIES[key] for key in keys}


def students_dict(*keys):
    return {ENTITIES[key].student_id: ENTITIES[key] for key in keys}
