"""
(Pure?) functions extracting information from world state
"""
import random

# TODO: generalize task selectors (uniform treatment without duplicite code,
#       allow for model parameters)

# TODO: create annotator to replace some parameters for defined parts of the
#       store, e.g. @extract_state(tasks=state.entities.tasks, ...)
#       ? but consider testability ?


def select_random_task(state, context):
    tasks = state.entities.tasks
    random.seed(context.randomness_seed)
    selected_task = random.choice(tasks)
    return selected_task


def select_task_in_fixed_order(state, student_id):
    pass


def compute_tasks_statistics(state):
    # NOTE: Alternative approach is to extract information by reducing series
    # of actions (see reducers)
    tasks = state.entities.tasks
    task_instances = state.entities.task_instances
    # TODO...
