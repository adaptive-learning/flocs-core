""" Pure functions extracting information from the world state
"""
import random


def select_random_task(state, student_id):
    tasks = state['entities.tasks']
    randomness_seed = state['context.randomness_seed']
    random.seed(randomness_seed)
    task_ids = list(tasks.keys())
    selected_task_id = random.choice(task_ids)
    return selected_task_id


def select_task_in_fixed_order(state, student_id):
    raise NotImplementedError
