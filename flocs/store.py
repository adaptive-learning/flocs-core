"""
State of the world representation
"""
from collections import namedtuple
from flocs import actions

class Store:
    def __init__(self, reducer):
        self.actions = []
        self.state = ()

    def append_action(self, action):
        self.actions.append(action)


GlobalState = namedtuple('GlobalState', [
    'entities',
])


Entities = namedtuple('Entities', [
    'students',
    'tasks',
    'task_instances',
])


TaskInstance = namedtuple('TaskInstance', [
    'task_instance_id',
    'student_id',
    'task_id',
    'solved',
    'given_up',
])


TaskStats = namedtuple('TaskStats', [
    'task_id',
    'started_count',
    'solved_count',
    'given_up_count',
])


## reducers (TODO: move them to separate module reducers.py)

def reduce_global_state(action, state):
    next_state = GlobalState(
        entities=reduce_entities(action, state.entities),
    )
    return next_state


def reduce_entities(action, state):
    next_state = Entities(
        students=reduce_students(action, state.students),
        tasks=reduce_students(action, state.tasks),
        task_instances=reduce_students(action, state.task_instances),
    )
    return next_state


def reduce_task_instances(action, task_instances):
    if isinstance(action, actions.StartTaskInstance):
        pass  # TODO
    elif isinstance(action, actions.SolveTaskInstance):
        task_instance = task_instances[action.task_instance_id]
        updated_task_instance = task_instance._replace(solved=True)
        return replace(task_instances, action.task_instance_id, updated_task_instance)
    elif isinstance(action, actions.GiveUpTaskInstance):
        # TODO: DRY
        task_instance = task_instances[action.task_instance_id]
        updated_task_instance = task_instance._replace(given_up=True)
        return replace(task_instances, action.task_instance_id, updated_task_instance)
    else:
        return task_instances


# Example of reducer which probably shouldn't be part of the store, but should
# be run on a historical stream of actions when needed)

def reduce_tasks_stats(action, stats='TBA??'):
    if isinstance(action, actions.StartTaskInstance):
        # TODO: abstract the following lines (e.g. update_on_index)
        record = stats[action.task_id]
        updated_record = record._replace(started_count=record.started_count + 1)
        updated_stats = replace(stats, action.task_id, updated_record)
        return updated_stats
    # TODO: other actions -> DRY
    else:
        return stats






# quick utils

def replace(t, i, new_value):
    return t[:i] + (new_value,) + t[i+1:]
