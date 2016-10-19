""" Pure functions extracting information from the world state
"""
import random
from flocs.entities import Student, Task, TaskInstance
from flocs.state import create_tasks_dict


def select_random_task(state, student_id):
    del student_id  # intentionally unused argument
    tasks = state['entities.tasks']
    randomness_seed = state['context.randomness_seed']
    random.seed(randomness_seed)
    task_ids = list(tasks.keys())
    selected_task_id = random.choice(task_ids)
    return selected_task_id


def select_task_in_fixed_order(state, student_id):
    last_task_instance_id = state.entities[Student][student_id].last_task_instance
    last_task_id = state.entities[TaskInstance][last_task_instance_id].task_id

    task_id_list = []
    for task in state.entities[Task]:
        task_id_list.append(task)
    task_id_list.sort()

    index = task_id_list.index(last_task_id)
    if index == len(task_id_list) - 1:
        raise ValueError('last task reached, there is no next task')
    selected_task_id = task_id_list[index + 1]
    return selected_task_id
