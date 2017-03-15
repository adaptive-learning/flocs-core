"""Functions describing how the world changes after various actions
"""
from collections import defaultdict, ChainMap
from inspect import signature
from . import entities
from .state import State
from .actions import ActionType
from .entities import Action, Student, TaskSession, SeenInstruction


def reduce_state(state, action):
    """Reduce the whole state of the world
    """
    return State(
        entities=reduce_entities(state.entities, action),
        time=action.time,
        randomness=action.randomness,
        version=action.version,
    )


def reduce_entities(old_entities, action):
    new_entities = {
        entity_type: reduce_entity(entity_type, entity_dict, action)
        for entity_type, entity_dict in old_entities.items()
    }
    return new_entities


def reduce_entity(entity_type, entity_dict, action):
    if entity_type == Action:
        return entity_dict.set(action)
    reducer = ENTITY_REDUCERS[entity_type][action.type]
    adapted_reducer = extracting_data_context(reducer)
    next_entity_dict = adapted_reducer(
        entity_dict=entity_dict,
        data=action.data,
        context={}  # TODO: find out how to pass context (if needed)
    )
    return next_entity_dict


def extracting_data_context(reducer):
    data_keys = extract_parameters(reducer, skip=1)
    def adapted_reducer(entity_dict, data, context):
        data_with_context = ChainMap(data, context)
        data_kwargs = {key: data_with_context[key] for key in data_keys}
        return reducer(entity_dict, **data_kwargs)
    return adapted_reducer


def extract_parameters(fn, skip=0):
    return tuple(signature(fn).parameters)[skip:]


def identity_defaultdict(dictionary=None):
    dictionary = dictionary or {}
    return defaultdict(lambda: identity_reducer, dictionary)


def identity_reducer(state):
    return state


def create_student(students, student_id):
    student = Student(student_id=student_id,
                      last_task_session_id=None,
                      credits=0)
    return students.set(student)


def create_task_session(task_sessions, task_session_id, student_id, task_id):
    task_session = TaskSession(
        task_session_id=task_session_id,
        student_id=student_id,
        task_id=task_id,
        solved=False,
        given_up=False,
    )
    return task_sessions.set(task_session)


def update_last_task_session_id(students, task_session_id, student_id, task_id):
    del task_id  # intentionally unused argument
    student = students[student_id]
    updated_student = student._replace(last_task_session_id=task_session_id)
    return students.set(updated_student)


def solve_task_session(task_sessions, task_session_id):
    task_session = task_sessions[task_session_id]
    updated_task_session = task_session._replace(solved=True)
    return task_sessions.set(updated_task_session)


def give_up_task_session(task_sessions, task_session_id):
    task_session = task_sessions[task_session_id]
    updated_task_session = task_session._replace(given_up=True)
    return task_sessions.set(updated_task_session)


def increase_started_count(stats, task_id):
    task_stats = stats[task_id]
    updated_started_count = task_stats.started_count + 1
    updated_task_stats = task_stats._replace(started_count=updated_started_count)
    return stats.set(updated_task_stats)


def increase_solved_count(stats, task_id):
    task_stats = stats[task_id]
    updated_solved_count = task_stats.solved_count + 1
    updated_task_stats = task_stats._replace(solved_count=updated_solved_count)
    return stats.set(updated_task_stats)


def increase_given_up_count(stats, task_id):
    task_stats = stats[task_id]
    updated_given_up_count = task_stats.given_up_count + 1
    updated_task_stats = task_stats._replace(given_up_count=updated_given_up_count)
    return stats.set(updated_task_stats)


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
ALWAYS_IDENTITY = identity_defaultdict()

# it is made explitic which entities are not changing to get a guarantee that
# an entity key corresponds to an actual entity (e.g. not just a string)
ENTITY_REDUCERS = {
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
    entities.TaskStats: identity_defaultdict({
        ActionType.start_task: increase_started_count,
        ActionType.solve_task: increase_solved_count,
        ActionType.give_up_task: increase_given_up_count,
    }),
    entities.Block: ALWAYS_IDENTITY,
    entities.Category: ALWAYS_IDENTITY,
    entities.Instruction: ALWAYS_IDENTITY,
    entities.Level: ALWAYS_IDENTITY,
    entities.Toolbox: ALWAYS_IDENTITY,
    entities.Task: ALWAYS_IDENTITY,
}
