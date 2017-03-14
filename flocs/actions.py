"""Actions represent events and interactions in the world we want to model

Future actions include:
    - StartSession
    - AttemptTask
    - ReportFlow
"""
from collections import namedtuple
from enum import Enum
from flocs.context import generate_id_if_not_set
from flocs.meta import META


class Action(namedtuple('Action', ['type', 'data', 'context', 'meta'])):
    """Action represents an event or an interaction in the world we model

    Args:
        type: one of the finitely many types (ActionType string or None)
        data: deatils about this specific action
        context: part of the state changing continuously (e.g. time)
        meta: information about how to interpret the action (e.g. package version)
    """
    __slots__ = ()

    @staticmethod
    def create(type=None, data=None, context=None):
        """Create an action with common meta information
        """
        # pylint:disable=redefined-builtin
        return Action(type=type, data=data, context=context, meta=META.copy())

    def at(self, state):
        """Set action within the context of given state

        >>> from .state import State
        >>> state = State(entities='e', context='c', meta='m')
        >>> Action('T', 'D', None, 'M').at(state)
        Action(type='T', data='D', context='c', meta='M')
        """
        return self._replace(context=state.context)


class ActionType(str, Enum):
    """Namespace for available action types constants
    """
    create_student = 'create-student'
    start_task = 'start-task'
    solve_task = 'solve-task'
    give_up_task = 'give-up-task'
    see_instruction = 'see-instruction'


def create_student(student_id=None):
    """A new student exists in the world
    """
    return Action.create(
        type=ActionType.create_student,
        data={
            'student_id': generate_id_if_not_set(student_id),
        },
    )


def start_task(student_id, task_id, task_session_id=None):
    """A student starts working on a task
    """
    return Action.create(
        type=ActionType.start_task,
        data={
            'task_session_id': generate_id_if_not_set(task_session_id),
            'student_id': student_id,
            'task_id': task_id,
        },
    )


def solve_task(task_session_id):
    """A student has solved a task
    """
    return Action.create(
        type=ActionType.solve_task,
        data={
            'task_session_id': task_session_id,
        },
    )


def give_up_task(task_session_id):
    """A student has given up a task
    """
    return Action.create(
        type=ActionType.give_up_task,
        data={
            'task_session_id': task_session_id,
        },
    )


def see_instruction(student_id, instruction_id, seen_instruction_id=None):
    """ Student has seen instruction
    """
    return Action.create(
        type=ActionType.see_instruction,
        data={
            'seen_instruction_id': generate_id_if_not_set(seen_instruction_id),
            'student_id': student_id,
            'instruction_id': instruction_id,
        },
    )



EMPTY_ACTION = Action.create()
