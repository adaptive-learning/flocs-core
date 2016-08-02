""" Techniques for task recommendation
"""
from collections import namedtuple
from functools import partial


# TODO: builder design patter for recommender

def recommend_task(student, tasks, criteria):
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

## -- somewhere else  ? --
#level_date_recommender = partial(
#    recommend_task,
#    criteria=[
#        Criterion(weight=1, func=TBA)
#        Criterion(weight=2, func=TBA)
#    ]
#)
