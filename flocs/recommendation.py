""" Techniques for task recommendation

Task recommender protocol:
    - args: state, student_id
    - return: recommneded task_id
"""
from collections import namedtuple
import random


Criterion = namedtuple('Criterion', ['weight', 'fn'])

default_fixed_order = (
    'one-step-forward',
    'diamond-on-right',
    'wormhole-demo',
    'shot',
    'ladder',
)


def randomly(state, student_id):
    """ Select task completely at random
    """
    del student_id  # intentionally unused argument
    random.seed(state.context.randomness)
    task_ids = list(state.tasks.keys())
    selected_task_id = random.choice(task_ids)
    return selected_task_id


def multicriteria(state, student_id, criteria):
    """ Recommend task linearly combining several criteria

    Usage:
    ```
    level_date_recommender = partial(
        multicriteria,
        criteria=[
            Criterion(weight=1, fn=level_difference)
            Criterion(weight=5, fn=time_from_last_solution)
        ]
    )
    ```
    """
    score_task = lambda task_id: sum(
        criterion.weight * criterion.fn(state, student_id, task_id)
        for criterion in criteria)
    best_task_id = max(state.tasks, key=score_task)
    return best_task_id


def fixed_order(state, student_id, order=default_fixed_order):
    """ Recommend task in a given fixed order

    It only moves to next task in the order when the current task is solved.
    (In particular, it's not enough to start solving the task. Giving up
    doesn't convice the recommender to move to the next task neither.)

    Additional args:
        - order: list of task IDs
    """
    solved_task_sessions = state.task_sessions.filter(
        student_id=student_id,
        solved=True)
    solved_task_ids = {ts.task_id for ts in solved_task_sessions.values()}
    for task_id in order:
        if task_id not in solved_task_ids:
            return task_id
    raise ValueError('last task reached, there is no next task')


def fixed_then_random(state, student_id):
    """ Select task in fixed order, then from other unsolved, then from all

    It never selects the previously-solved task
    """
    try:
        return fixed_order(state, student_id)
    except ValueError:
        task_ids = list(state.tasks.keys())
        solved_task_sessions = state.task_sessions.filter(
            student_id=student_id,
            solved=True)
        solved_task_ids = [ts.task_id for ts in solved_task_sessions.values()]
        unsolved_task_ids = [t_id for t_id in task_ids if t_id not in solved_task_ids]
        random.seed(state.context.randomness)
        if unsolved_task_ids:
            selected_task_id = random.choice(unsolved_task_ids)
            return selected_task_id
        else:
            last_task_session = solved_task_sessions.order_by('end').last()
            last_task_id = last_task_session.task_id
            task_ids.remove(last_task_id)
            selected_task_id = random.choice(task_ids)
            return selected_task_id
