""" Actions represent intreactions and events in the world which we model

Action is a dict containing:
    - type
    - data
    - context
    - meta

This module defines available action types, associated data and action creators.


Usage:
    - create action of known type and data (optionally with meta and context)
    actions.solve_task(task_instance_id=0)

Future actions include:
    - ChangePackageVersion
    - StartSession
    - AttemptTask
    - ReportFlow
"""

# TODO: consider using modules for namespaces instead of classes
# TODO: describe semantics of each action, if neccessary

class ActionType:
    """Namespace for available action types
    """
    create_student = 'create_student'
    start_task = 'start_task'
    solve_task = 'solve_task'
    give_up_task = 'give_up_task'


class ActionCreators:
    """Namespace for functions creating action dictionaries
    """
    # TODO: a decorator to factor out common functionality from the following creators

    @staticmethod
    def create_student(student_id=None, context=None, meta=None):
        # TODO: if student id is None, generate it (?)
        data = {
            'student_id': student_id,
        }
        return {
            'type': ActionType.create_student,
            'data': data,
            'context': context,
            'meta': meta,
        }

    @staticmethod
    def start_task(student_id, task_id, task_instance_id=None, context=None, meta=None):
        # TODO: if task_instance_id is None, generate it (?)
        data = {
            'task_instance_id': task_instance_id,
            'student_id': student_id,
            'task_id': task_id,
        }
        return {
            'type': ActionType.start_task,
            'data': data,
            'context': context,
            'meta': meta,
        }

    @staticmethod
    def solve_task(task_instance_id, context=None, meta=None):
        data = {
            'task_instance_id': task_instance_id,
        }
        return {
            'type': ActionType.solve_task,
            'data': data,
            'context': context,
            'meta': meta,
        }
