""" Functions describing how the world changes after various actions
"""
from collections import ChainMap
from inspect import signature
from .action_types import ActionType
from .entities import Student, TaskInstance

# --------------------------------------------------------------------------

def data_extracting(subreducer):
    """Decorate subreducer to take a substate and data dict
    >>> @data_extracting
    ... def subreducer(substate, a, c): return substate, a, c
    >>> subreducer('X', data={'a': 1, 'b': 2, 'c': 3})
    ('X', 1, 3)
    """
    data_keys = tuple(signature(subreducer).parameters)[1:]
    def wrapped_subreducer(substate, data):
        data_kwargs = {key: data[key] for key in data_keys}
        return subreducer(substate, **data_kwargs)
    return wrapped_subreducer

# --------------------------------------------------------------------------

def reduce_students(students, action):
    reducers = {
        ActionType.create_student: create_student,
    }
    reduce_action = reducers.get(action.type, lambda state: state)
    next_state = data_extracting(reduce_action)(students, data=action.data)
    return next_state


def reduce_task_instances(task_instances, action):
    reducers = {
        ActionType.start_task: create_task_instance,
        ActionType.solve_task: solve_task_instance,
        ActionType.give_up_task: give_up_task_instance,
    }
    reduce_action = reducers.get(action.type, lambda state: state)
    next_state = data_extracting(reduce_action)(task_instances, data=action.data)
    return next_state


def reduce_tasks_stats(stats, action):
    reducers = {
        ActionType.start_task: increase_started_count,
        ActionType.solve_task: increase_solved_count,
        ActionType.give_up_task: increase_given_up_count,
    }
    reduce_action = reducers.get(action.type, lambda state: state)
    next_state = data_extracting(reduce_action)(stats, data=action.data)
    return next_state


# --------------------------------------------------------------------------


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


def solve_task_instance(task_instances, task_instance_id):
    task_instance = task_instances[task_instance_id]
    updated_task_instance = task_instance._replace(solved=True)
    return ChainMap({task_instance_id: updated_task_instance}, task_instances)


def give_up_task_instance(task_instances, task_instance_id):
    task_instance = task_instances[task_instance_id]
    updated_task_instance = task_instance._replace(given_up=True)
    return ChainMap({task_instance_id: updated_task_instance}, task_instances)

# --------------------------------------------------------------------------

def combine_reducers(reducers):
    """ Return a reducer that action delegates to all given reducers

    Args:
        reducers: mapping from substate key to a reducer function
                  (or to None if it should stay constant)
    """
    def reducer(state, action):
        next_state = {
            key: (reducer(state[key], action) if reducer is not None else state[key])
            for key, reducer in reducers.items()
        }
        return next_state
    return reducer

WORLD_REDUCER = combine_reducers({
    'meta.version': None,
    'entities.tasks': None,
    'entities.students': reduce_students,
    'entities.task_instances': reduce_task_instances,
    'context.time': None,
    'context.randomness_seed': None,
    })
