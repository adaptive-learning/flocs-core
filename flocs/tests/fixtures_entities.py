"""Entities objects for testing purposes
"""
from flocs.entities import TaskInstance


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
}


def task_instances_dict(*keys):
    return {ENTITIES[key].task_instance_id: ENTITIES[key] for key in keys}
