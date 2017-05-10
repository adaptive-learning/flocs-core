from collections import namedtuple

TaskStats = namedtuple('TaskStats', [
    'task_id',
    'started_count',
    'solved_count',
])


def get_level(state, task_id):
    """ Throws KeyError if task or category for the task could not have been located in state.
    """
    task = state.tasks[task_id]
    category = state.categories[task.category_id]
    level = state.levels[category.level_id]
    return level


def get_credits(state, task_id):
    try:
        level_id = get_level(state, task_id).level_id
        return level_id
    except KeyError:
        return 0


def get_earned_credits(state, student_id, task_id):
    """ Return number of credits earned for solving given task by given student

    Currently, the number of credits is simply equal to the level of category
    which this task belongs to. It is 0 if the student has already solved this
    task before.
    """
    solved_before = state.task_sessions \
        .filter(student_id=student_id, task_id=task_id, solved=True) \
        .exists()
    if solved_before:
        return 0
    return get_credits(state, task_id)


def get_task_stats(state, task_id):
    raise NotImplementedError
