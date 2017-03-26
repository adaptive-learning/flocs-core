""" Pure functions extracting information from the world state
"""
from collections import namedtuple
from operator import attrgetter
from flocs.entities import Student, TaskSession, SeenInstruction, Level


StudentInfo = namedtuple('StudentInfo', [
    'student_id',
    'seen_instructions',
    'task_sessions',
])


TaskStats = namedtuple('TaskStats', [
    'task_id',
    'started_count',
    'solved_count',
    'given_up_count',
])


def get_student_info(state, student_id):
    info = StudentInfo(
        student_id=student_id,
        seen_instructions=state.entities[SeenInstruction].filter(student_id=student_id),
        task_sessions=state.entities[TaskSession].filter(student_id=student_id))
    return info


def get_level(state, student_id):
    student = state.entities[Student][student_id]
    levels = state.entities[Level]
    level = max([level for level in levels.values() if student.credits - level.credits >= 0],
                key=attrgetter('credits'))
    return level


def get_unspent_credits(state, student_id):
    student = state.entities[Student][student_id]
    level = get_level(state, student_id)
    return student.credits - level.credits


def get_task_stats(state, task_id):
    raise NotImplementedError
