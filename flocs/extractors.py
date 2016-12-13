""" Pure functions extracting information from the world state
"""
from functools import partial
import random
from flocs.entities import Student, Task, TaskSession


def select_random_task(state, student_id):
    del student_id  # intentionally unused argument
    tasks = state.entities[Task]
    randomness_seed = state.context['randomness']
    random.seed(randomness_seed)
    task_ids = list(tasks.keys())
    selected_task_id = random.choice(task_ids)
    return selected_task_id


def general_select_task_in_fixed_order(state, student_id, order):
    """ Must be called partially applied (without order parameter) to satisfy the contract
    """
    last_task_session_id = state.entities[Student][student_id].last_task_session
    if last_task_session_id is not None:
        last_task_id = state.entities[TaskSession][last_task_session_id].task_id
        index = order.index(last_task_id)
    else:
        index = -1

    if index == len(order) - 1:
        raise ValueError('last task reached, there is no next task')
    selected_task_id = order[index + 1]
    return selected_task_id


select_task_in_fixed_order = partial(
    general_select_task_in_fixed_order,
    order=[
        'one-step-forward',
        'three-steps-forward',
        'turning-left',
        'turning-right-and-left',
        'diamond-on-right',
        'shot',
        'shooting',
        'zig-zag',
        'ladder',
        'on-yellow-to-left',
    ])
