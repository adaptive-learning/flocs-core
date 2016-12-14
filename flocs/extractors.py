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
    """Recommend task in a given fixed order

    It only moves to next task in the order when the current task is solved.
    (In particular, it's not enough to start solving the stask. But giving up
    doesn't convice the recommender to move to the next task neither.)

    This is a general recommeder, to get a specific recommender which satisfy
    recommender contract, `order` parameter (list of Ids) must be applied.
    """
    task_index = 0
    last_task_session_id = state.entities[Student][student_id].last_task_session
    if last_task_session_id:
        last_task_session = state.entities[TaskSession][last_task_session_id]
        last_task_id = last_task_session.task_id
        task_index = order.index(last_task_id)
        if last_task_session.solved:
            task_index += 1
    if task_index == len(order):
        raise ValueError('last task reached, there is no next task')
    selected_task_id = order[task_index]
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
