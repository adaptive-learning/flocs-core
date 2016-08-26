"""Actions represent events and interactions in the world we want to model

Future actions include:
    - ChangePackageVersion
    - StartSession
    - AttemptTask
    - ReportFlow
"""
from flocs.actions import action_creator, get_registered_action_types
from flocs.context import generate_random_id


@action_creator
def create_student(student_id=None, context=None):
    """A new student exists in the world

    >>> create_student(student_id=16)
    Action(type='create_student', data={'student_id': 16}, context=None, meta=None)
    """
    student_id = student_id if student_id is not None else generate_random_id(context)
    return {
        'student_id': student_id,
    }


@action_creator
def start_task(student_id, task_id, task_instance_id=None, context=None):
    task_instance_id = task_instance_id if task_instance_id is not None \
                        else generate_random_id(context)
    return {
        'task_instance_id': task_instance_id,
        'student_id': student_id,
        'task_id': task_id,
    }


@action_creator
def solve_task(task_instance_id, context=None):
    return {
        'task_instance_id': task_instance_id,
    }


@action_creator
def give_up_task(task_instance_id, context=None):
    return {
        'task_instance_id': task_instance_id,
    }


ALL_ACTION_TYPES = get_registered_action_types()
