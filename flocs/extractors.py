""" Pure functions extracting information from the world state
"""
from collections import namedtuple
from datetime import timedelta
from itertools import accumulate, chain
from uuid import uuid4

TaskStats = namedtuple('TaskStats', [
    'task_id',
    'started_count',
    'solved_count',
])


def new_id(state):
    if state.context.new_id == 'uuid':
        return uuid4()
    if state.context.new_id == 'seq':
        return state.total_entities()
    return state.context.new_id


def get_student_id_for_task_session(state, task_session_id):
    task_session = state.task_sessions[task_session_id]
    return task_session.student_id


def get_task_id_for_task_session(state, task_session_id):
    task_session = state.task_sessions[task_session_id]
    return task_session.task_id


def get_current_session_id(state, student_id, new_if_none=True):
    session = state.sessions.filter(student_id=student_id).order_by('end').last()
    if not session or session_too_old(session, state.context.time):
        return new_id(state) if new_if_none else None
    return session.session_id


def session_too_old(session, time):
    time_passed = time - session.end
    too_old = time_passed >= timedelta(hours=5)
    return too_old


def is_solved(state, student_id, task_id):
    solved_task_sessions = state.task_sessions.filter(student_id=student_id,
                                                      task_id=task_id,
                                                      solved=True)
    return solved_task_sessions.exists()


def get_time(state, student_id, task_id):
    """ Best time if student has solved the task, otherwise just the last time
    """
    task_sessions = state.task_sessions.filter(student_id=student_id, task_id=task_id)
    solved_task_sessions = task_sessions.filter(solved=True)
    if solved_task_sessions.exists():
        times = [ts.time_spent for ts in solved_task_sessions.values()]
        return min(times)
    last_task_session = task_sessions.order_by('end').last()
    return last_task_session.time_spent if last_task_session else None


def get_needed_credits_for_level(state, level_id):
    for level, credits in needed_credits_for_levels(state):
        if level.level_id == level_id:
            return credits
    return 0


def needed_credits_for_levels(state):
    levels = state.levels.order_by('level_id').values()
    # 0 credits needed to already be on the first level
    needed_credits = accumulate(chain([0], levels), lambda c, l: c + l.credits)
    # last accumulated value is not used - one can't go beyond the last level
    return zip(levels, needed_credits)


def get_task_stats(state, task_id):
    raise NotImplementedError


def get_next_snapshot_order(state, task_session_id):
    snapshots = state.program_snapshots.filter(task_session_id=task_session_id)
    return len(snapshots) + 1


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
    try:
        task = state.tasks[task_id]
        category = state.categories[task.category_id]
    except KeyError:
        return 0
    level = category.level_id
    credits = level
    return credits
