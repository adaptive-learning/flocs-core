""" Actions represent intreactions and events in the world we want to model
"""
from collections import namedtuple
from enum import Enum
from flocs.context import generate_random_id


# TODO: consider using modules for namespaces instead of classes
# TODO: describe semantics of each action, if neccessary

Action = namedtuple('Action', ['type', 'data', 'context', 'meta'])


class ActionType(str, Enum):
    """Namespace for available action types
    """
    create_student = 'create_student'
    start_task = 'start_task'
    solve_task = 'solve_task'
    give_up_task = 'give_up_task'

    #Future actions include:
    #    - ChangePackageVersion
    #    - StartSession
    #    - AttemptTask
    #    - ReportFlow


class ActionCreators:
    """Namespace for functions creating actions
    """
    # TODO: a decorator to factor out common functionality from the following creators

    @staticmethod
    def create_student(student_id=None, context=None, meta=None):
        student_id = student_id if student_id is not None else generate_random_id(context)
        data = {
            'student_id': student_id,
        }
        return Action(
            type=ActionType.create_student,
            data=data,
            context=context,
            meta=meta,
        )

    @staticmethod
    def start_task(student_id, task_id, task_instance_id=None, context=None, meta=None):
        task_instance_id = task_instance_id if task_instance_id is not None \
                           else generate_random_id(context)
        data = {
            'task_instance_id': task_instance_id,
            'student_id': student_id,
            'task_id': task_id,
        }
        return Action(
            type=ActionType.start_task,
            data=data,
            context=context,
            meta=meta,
        )

    @staticmethod
    def solve_task(task_instance_id, context=None, meta=None):
        data = {
            'task_instance_id': task_instance_id,
        }
        return Action(
            type=ActionType.solve_task,
            data=data,
            context=context,
            meta=meta,
        )

    @staticmethod
    def give_up_task(task_instance_id, context=None, meta=None):
        data = {
            'task_instance_id': task_instance_id,
        }
        return Action(
            type=ActionType.give_up_task,
            data=data,
            context=context,
            meta=meta,
        )
