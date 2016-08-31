""" Functions describing how the world changes after various actions
"""
from collections import ChainMap, defaultdict
from inspect import signature
from . import entities
from .state import State
from .actions import ActionType
from .entities import Student, TaskInstance


def reduce_state(state, action):
    """Reduce the whole state of the world
    """
    return State(
        entities=reduce_entities(state.entities, action),
        context=action.context,
        meta=action.meta,
    )


def reduce_entities(entities, action):
    new_entities = {
        entity_type: reduce_entity(entity_type, entity_dict, action)
        for entity_type, entity_dict in entities.items()
    }
    return new_entities


def reduce_entity(entity_type, entity_dict, action):
    reducer = ENTITY_REDUCERS[entity_type][action.type]
    adapted_reducer = extracting_data_context(reducer)
    next_entity_dict = adapted_reducer(
        entity_dict=entity_dict,
        data=action.data,
        context=action.context,
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
    student = Student(student_id=student_id)
    return ChainMap({student_id: student}, students)


def create_task_instance(task_instances, task_instance_id, student_id, task_id):
    task_instance = TaskInstance(
        task_instance_id=task_instance_id,
        student_id=student_id,
        task_id=task_id,
        solved=False,
        given_up=False,
    )
    return ChainMap({task_instance_id: task_instance}, task_instances)


def solve_task_instance(task_instances, task_instance_id):
    task_instance = task_instances[task_instance_id]
    updated_task_instance = task_instance._replace(solved=True)
    return ChainMap({task_instance_id: updated_task_instance}, task_instances)


def give_up_task_instance(task_instances, task_instance_id):
    task_instance = task_instances[task_instance_id]
    updated_task_instance = task_instance._replace(given_up=True)
    return ChainMap({task_instance_id: updated_task_instance}, task_instances)


def increase_started_count(stats, task_id):
    task_stats = stats[task_id]
    updated_started_count = task_stats.started_count + 1
    updated_task_stats = task_stats._replace(started_count=updated_started_count)
    return ChainMap({task_id: updated_task_stats}, stats)


def increase_solved_count(stats, task_id):
    task_stats = stats[task_id]
    updated_solved_count = task_stats.solved_count + 1
    updated_task_stats = task_stats._replace(solved_count=updated_solved_count)
    return ChainMap({task_id: updated_task_stats}, stats)


def increase_given_up_count(stats, task_id):
    task_stats = stats[task_id]
    updated_given_up_count = task_stats.given_up_count + 1
    updated_task_stats = task_stats._replace(given_up_count=updated_given_up_count)
    return ChainMap({task_id: updated_task_stats}, stats)


# --------------------------------------------------------------------------
ALWAYS_IDENTITY = identity_defaultdict()

# it is made explitic which entities are not changing to get a guarantee that
# an entity key corresponds to an actual entity (e.g. not just a string)
ENTITY_REDUCERS = {
    entities.Student: identity_defaultdict({
        ActionType.create_student: create_student,
    }),
    entities.TaskInstance: identity_defaultdict({
        ActionType.start_task: create_task_instance,
        ActionType.solve_task: solve_task_instance,
        ActionType.give_up_task: give_up_task_instance,
    }),
    entities.TaskStats: identity_defaultdict({
        ActionType.start_task: increase_started_count,
        ActionType.solve_task: increase_solved_count,
        ActionType.give_up_task: increase_given_up_count,
    }),
    entities.Task: ALWAYS_IDENTITY,
}
