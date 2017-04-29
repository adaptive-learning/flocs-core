""" Pure functions extracting information from the world state
"""
from collections import namedtuple
from datetime import timedelta
from itertools import accumulate, chain
from math import inf
from uuid import uuid4
from flocs.entities import Level
from flocs import recommendation


PracticeOverview = namedtuple('PracticeOverview', [
    'level',
    'credits',
    'active_credits',
    'instructions',
    'tasks',
    'recommendation',
])


Recommendation = namedtuple('Recommendation', [
    'available',
    'task_id',
])


StudentInstruction = namedtuple('StudentInstruction', [
    'instruction_id',
    'seen',
])


StudentTask = namedtuple('StudentTask', [
    'task_id',
    'solved',
    'time',
])


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


def get_recommendation(state, student_id):
    task_id = recommendation.fixed_then_random(state, student_id)
    return Recommendation(available=True, task_id=task_id)


def get_practice_overview(state, student_id):
    student = state.students[student_id]
    overview = PracticeOverview(
        level=get_level(state, student_id).level_id,
        credits=student.credits,
        active_credits=get_active_credits(state, student_id),
        instructions=get_student_instructions(state, student_id),
        tasks=get_student_tasks(state, student_id),
        recommendation=get_recommendation(state, student_id),
    )
    return overview


def get_student_instructions(state, student_id):
    seen_instructions = state.seen_instructions.filter(student_id=student_id)
    # TODO: allow for student.seen_instructions
    student_instructions = [
        StudentInstruction(
            instruction_id=instruction_id,
            seen=seen_instructions.filter(instruction_id=instruction_id).exists(),
        )
        for instruction_id in state.instructions
    ]
    return student_instructions



def get_student_tasks(state, student_id):
    student_tasks = [
        StudentTask(
            task_id=task_id,
            solved=is_solved(state, student_id, task_id),
            time=get_time(state, student_id, task_id),
        )
        for task_id in state.tasks
    ]
    return student_tasks


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


def get_level(state, student_id):
    if not state.levels:
        return Level(level_id=0, credits=0)
    student = state.students[student_id]
    level = Level(level_id=0, credits=0)
    levels = levels_with_total_credits(state)
    for next_level, needed_credits in chain(levels, [(None, inf)]):
        if student.credits >= needed_credits:
            level = next_level
        else:
            return level


def get_active_credits(state, student_id):
    student = state.students[student_id]
    level = get_level(state, student_id)
    level_total_credits = get_level_total_credits(state, level.level_id)
    return student.credits - level_total_credits


def get_level_total_credits(state, level_id):
    for level, credits in levels_with_total_credits(state):
        if level.level_id == level_id:
            return credits
    return 0


def levels_with_total_credits(state):
    levels = state.levels.order_by('level_id').values()
    total_credits = accumulate(chain([0], levels), lambda c, l: c + l.credits)
    next(total_credits)  # omit the added 0
    return zip(levels, total_credits)


def get_task_stats(state, task_id):
    raise NotImplementedError


def get_next_snapshot_order(state, task_session_id):
    snapshots = state.program_snapshots.filter(task_session_id=task_session_id)
    return len(snapshots) + 1
