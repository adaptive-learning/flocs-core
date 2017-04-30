""" Functions describing how the world changes after various actions
"""
from collections import ChainMap, defaultdict
from inspect import signature
from . import entities
from .actions import ActionType
from .entities import Session, Student, TaskSession, SeenInstruction, ProgramSnapshot


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
            action_types = [action_type] if isinstance(action_type, ActionType) else action_type
            assert action.type in action_types
            assert entity_map.entity_class == entity_class or not entity_map.entity_class
            data_context = ChainMap(action.data, {'context': action.context})
            kwarg_names = extract_parameters(fn, skip=1)
            kwargs = {name: data_context[name] for name in kwarg_names}
            return fn(entity_map, **kwargs)
        fn_wrapped.__name__ = fn.__name__
        fn_wrapped.__doc__ = fn.__doc__
        return fn_wrapped
    return reducer_decorator


def extract_parameters(fn, skip=0):
    return tuple(signature(fn).parameters)[skip:]


@reducer(entities.Session, ActionType.start_session)
def create_session(sessions, session_id, student_id, context):
    session = Session(
        session_id=session_id,
        student_id=student_id,
        start=context.time,
        end=context.time,
    )
    return sessions.set(session)


@reducer(entities.Session, ActionType.start_task)
def create_or_update_session(sessions, session_id, student_id, context):
    if session_id in sessions:
        session = sessions[session_id]._replace(end=context.time)
    else:
        session = Session(
            session_id=session_id,
            student_id=student_id,
            start=context.time,
            end=context.time,
        )
    # TODO: dry using create_session reducer (nontrivial because its signature
    # is modified by the @reducer decorator)
    return sessions.set(session)


@reducer(entities.Session, [ActionType.solve_task, ActionType.run_program, ActionType.edit_program])
def update_session_end(sessions, session_id, context):
    if session_id not in sessions:
        return sessions
    session = sessions[session_id]._replace(end=context.time)
    return sessions.set(session)


@reducer(entities.Student, ActionType.start_session)
def create_student_if_new(students, student_id):
    student = Student(student_id=student_id, credits=0)
    return students.set(student)


@reducer(entities.TaskSession, ActionType.start_task)
def create_task_session(task_sessions, task_session_id, student_id, task_id, context):
    task_session = TaskSession(
        task_session_id=task_session_id,
        student_id=student_id,
        task_id=task_id,
        solved=False,
        given_up=False,
        start=context.time,
        end=context.time,
    )
    return task_sessions.set(task_session)


@reducer(entities.TaskSession, ActionType.solve_task)
def solve_task_session(task_sessions, task_session_id, context):
    task_session = task_sessions[task_session_id]
    if task_session.solved:
        return task_sessions
    updated_task_session = task_session._replace(solved=True, end=context.time)
    return task_sessions.set(updated_task_session)


@reducer(entities.TaskSession, [ActionType.run_program, ActionType.edit_program])
def update_task_session_end(task_sessions, task_session_id, context):
    task_session = task_sessions[task_session_id]
    if task_session.solved:
        return task_sessions
    updated_task_session = task_session._replace(end=context.time)
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


@reducer(entities.ProgramSnapshot, ActionType.edit_program)
def take_snapshot_on_edit(snapshots, program_snapshot_id, task_session_id,
                          order, program, context):
    snapshot = ProgramSnapshot(
        program_snapshot_id=program_snapshot_id,
        task_session_id=task_session_id,
        order=order,
        time=context.time,
        program=program,
        execution=False,
        correct=None)
    return snapshots.set(snapshot)


@reducer(entities.ProgramSnapshot, ActionType.run_program)
def take_snapshot_on_execution(snapshots, program_snapshot_id, task_session_id,
                               order, program, correct, context):
    snapshot = ProgramSnapshot(
        program_snapshot_id=program_snapshot_id,
        task_session_id=task_session_id,
        order=order,
        time=context.time,
        program=program,
        execution=True,
        correct=correct)
    return snapshots.set(snapshot)


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
    entities.Session: identity_defaultdict({
        ActionType.start_session: create_session,
        ActionType.start_task: create_or_update_session,
        ActionType.edit_program: update_session_end,
        ActionType.run_program: update_session_end,
        ActionType.solve_task: update_session_end,
    }),
    entities.Student: identity_defaultdict({
        ActionType.start_session: create_student_if_new,
    }),
    entities.SeenInstruction: identity_defaultdict({
        ActionType.see_instruction: create_or_update_seen_instruction,
    }),
    entities.TaskSession: identity_defaultdict({
        ActionType.start_task: create_task_session,
        ActionType.edit_program: update_task_session_end,
        ActionType.run_program: update_task_session_end,
        ActionType.solve_task: solve_task_session,
        ActionType.give_up_task: give_up_task_session,
    }),
    entities.ProgramSnapshot: identity_defaultdict({
        ActionType.edit_program: take_snapshot_on_edit,
        ActionType.run_program: take_snapshot_on_execution,
    }),
    entities.Block: ALWAYS_IDENTITY,
    entities.Category: ALWAYS_IDENTITY,
    entities.Instruction: ALWAYS_IDENTITY,
    entities.Level: ALWAYS_IDENTITY,
    entities.Toolbox: ALWAYS_IDENTITY,
    entities.Task: ALWAYS_IDENTITY,
}
