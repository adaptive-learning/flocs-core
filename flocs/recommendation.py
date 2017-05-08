""" Techniques for task recommendation

Task recommender protocol:
    - args: state, student_id
    - return: recommneded task_id
"""
from collections import namedtuple
import random
from flocs.student_extractors import get_student_level

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


def random_by_level(state, student_id, decay_factor=2):
    """ Selects task randomly but the probability is distributed according to difference between student's and task's
    levels. There is a single exception it never selects the last solved task.

    Args:
        state: current world state
        student_id: id of the student to whom the recommendation is given
        decay_factor: factor of probability decay between levels

    Returns: id of the selected task

    """
    student_level = get_student_level(state, student_id).level_id
    solved_task_sessions = state.task_sessions.filter(
        student_id=student_id,
        solved=True)
    last_task_session = solved_task_sessions.order_by('end').last()
    last_task_id = last_task_session.task_id if last_task_session else None
    restricted_tasks = {last_task_id} if last_task_id else {}
    weighted_tasks, sum_of_weights = _exponentially_weighted_tasks(state, student_level, restricted_tasks, decay_factor)
    random.seed(state.context.randomness)
    number = random.randint(0, sum_of_weights - 1)
    return _roulette_wheel_selection(weighted_tasks, number)


def _exponentially_weighted_tasks(state, student_level, restricted_tasks, decay_factor):
    """ Gives weights to the tasks based on their levels. Tasks with level higher than the student's level as well as
    restricted tasks have weight equal to 0.

    Args:
        state: current world state
        student_level: student's level
        restricted_tasks: collection of task id's that should not we selected
        decay_factor: factor of probability decay between levels

    Returns: tuple with list of tuples with task id and weight and total sum of all weights across all tasks

    """
    weighted_tasks = []
    sum_of_weights = 0
    for task_id in state.tasks:
        task = state.tasks[task_id]
        task_level = state.categories[task.category_id].level_id
        weight = 0
        if task_id not in restricted_tasks and task_level <= student_level:
            weight = decay_factor ** task_level
        weighted_tasks.append((task_id, weight))
        sum_of_weights += weight
    return weighted_tasks, sum_of_weights


def _roulette_wheel_selection(weighted_tasks, number):
    """ Selects from the list based on weights and given random number

    Args:
        weighted_tasks: list of tuples with task id and weight
        number: randomly generated number between [0, sum of all weights)

    Returns: selected task id

    """
    if number < 0:
        raise ValueError("Number must be positive.")
    for task_id, weight in weighted_tasks:
        if number < weight:
            return task_id
        number -= weight
    raise ValueError("Number must be lass than the sum of all weights in the list.")
