""" Techniques for task recommendation
"""
from collections import namedtuple
from functools import partial


def recommend_task(student, tasks, criteria):
    """ Recommend task linarly combining several criteria

    Usage:
    ```
    level_date_recommender = partial(
        recommend_task,
        criteria=[
            Criterion(weight=1, func=level_difference)
            Criterion(weight=5, func=time_from_last_solution)
        ]
    )
    ```
    """
    score_task_w_context = partial(score_task, student=student, criteria=criteria)
    best_task = max(tasks, key=score_task_w_context)
    return best_task


def score_task(task, student, criteria):
    score = sum(
        criterion.weight * criterion.func(student, task)
        for criterion in criteria
    )
    return score


Criterion = namedtuple('Criterion', ['weight', 'func'])
