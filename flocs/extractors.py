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
    (In particular, it's not enough to start solving the stask. Giving up
    doesn't convice the recommender to move to the next task neither.)

    This is a general recommeder, to get a specific recommender which satisfy
    recommender contract, `order` parameter (list of Ids) must be applied.
    """
    solved_task_sessions = state.entities[TaskSession].filter(
        student_id=student_id,
        solved=True)
    solved_task_ids = {ts.task_id for ts in solved_task_sessions.values()}
    for task_id in order:
        if task_id not in solved_task_ids:
            return task_id
    raise ValueError('last task reached, there is no next task')


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


def select_task_fixed_then_random(state, student_id):
    """Select task in fixed order and when all are solved, select randomly
    """
    try:
        return select_task_in_fixed_order(state, student_id)
    except ValueError:
        return select_random_task(state, student_id)
