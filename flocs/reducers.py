""" Functions describing how the world changes after various actions
"""
from collections import ChainMap, defaultdict
from inspect import signature
from . import entities
from .actions import ActionType
from .context import StaticContext
from .entities import Student, TaskSession, SeenInstruction


def get(entity_class, action_type):
    """ Return a reducer for given entity class and action type
    """
    return _entity_reducer_map[entity_class][action_type]


def reducer(entity_class, action_type):
    """ Change function signature to accept whole action entity

    Additionaly, it checks that the function is called for declared entity map
    and action type
    """
    def reducer_decorator(fn):
        # Don't use @wraps, because it would retract new function signature
        def fn_wrapped(entity_map, action):
            assert action.type == action_type
            assert entity_map.entity_class == entity_class or not entity_map.entity_class
            context = StaticContext(time=action.time, randomness=action.randomness)
            data_context = ChainMap(action.data, {'context': context})
            kwarg_names = extract_parameters(fn, skip=1)
            kwargs = {name: data_context[name] for name in kwarg_names}
            return fn(entity_map, **kwargs)
        fn_wrapped.__name__ = fn.__name__
        fn_wrapped.__doc__ = fn.__doc__
        return fn_wrapped
    return reducer_decorator


def extract_parameters(fn, skip=0):
    return tuple(signature(fn).parameters)[skip:]


@reducer(entities.Student, ActionType.create_student)
def create_student(students, student_id):
    student = Student(student_id=student_id, last_task_session_id=None, credits=0)
    return students.set(student)


@reducer(entities.Student, ActionType.start_task)
def update_last_task_session_id(students, task_session_id, student_id):
    student = students[student_id]
    updated_student = student._replace(last_task_session_id=task_session_id)
    return students.set(updated_student)


@reducer(entities.TaskSession, ActionType.start_task)
def create_task_session(task_sessions, task_session_id, student_id, task_id):
    task_session = TaskSession(
        task_session_id=task_session_id,
        student_id=student_id,
        task_id=task_id,
        solved=False,
        given_up=False,
    )
    return task_sessions.set(task_session)


@reducer(entities.TaskSession, ActionType.solve_task)
def solve_task_session(task_sessions, task_session_id):
    task_session = task_sessions[task_session_id]
    updated_task_session = task_session._replace(solved=True)
    return task_sessions.set(updated_task_session)


@reducer(entities.TaskSession, ActionType.give_up_task)
def give_up_task_session(task_sessions, task_session_id):
    task_session = task_sessions[task_session_id]
    updated_task_session = task_session._replace(given_up=True)
    return task_sessions.set(updated_task_session)


@reducer(entities.SeenInstruction, ActionType.see_instruction)
def create_or_update_seen_instruction(seen_instructions, seen_instruction_id,
                                      student_id, instruction_id):
    """ Create record of new seen instruction for student-instruction pair.
        If it has already existed, nothing is changed (so seen_instruction_id
        is ignored in this case).
    """
    records = seen_instructions.filter(student_id=student_id, instruction_id=instruction_id)
    already_seen = len(records) > 0
    if already_seen:
        return seen_instructions
    seen_instruction = SeenInstruction(
        seen_instruction_id=seen_instruction_id,
        student_id=student_id,
        instruction_id=instruction_id,
    )
    updated_seen_instructions = seen_instructions.set(seen_instruction)
    return updated_seen_instructions


# --------------------------------------------------------------------------


def identity_defaultdict(dictionary=None):
    dictionary = dictionary or {}
    return defaultdict(lambda: identity_reducer, dictionary)


def identity_reducer(state, _action):
    return state


ALWAYS_IDENTITY = identity_defaultdict()


# it is made explitic which entities are not changing to get a guarantee that
# an entity key corresponds to an actual entity (e.g. not just a string)
_entity_reducer_map = {
    entities.Student: identity_defaultdict({
        ActionType.start_task: update_last_task_session_id,
        ActionType.create_student: create_student,
    }),
    entities.SeenInstruction: identity_defaultdict({
        ActionType.see_instruction: create_or_update_seen_instruction,
    }),
    entities.TaskSession: identity_defaultdict({
        ActionType.start_task: create_task_session,
        ActionType.solve_task: solve_task_session,
        ActionType.give_up_task: give_up_task_session,
    }),
    entities.Block: ALWAYS_IDENTITY,
    entities.Category: ALWAYS_IDENTITY,
    entities.Instruction: ALWAYS_IDENTITY,
    entities.Level: ALWAYS_IDENTITY,
    entities.Toolbox: ALWAYS_IDENTITY,
    entities.Task: ALWAYS_IDENTITY,
}
