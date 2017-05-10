from collections import namedtuple
from flocs.student import get_active_credits, get_instructions, get_tasks, get_level
from flocs.recommendation import random_by_level

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


def get_recommendation(state, student_id):
    task_id = random_by_level(state, student_id)
    return Recommendation(available=True, task_id=task_id)


def get_practice_overview(state, student_id):
    student = state.students[student_id]
    overview = PracticeOverview(
        level=get_student_level(state, student_id).level_id,
        credits=student.credits,
        active_credits=get_active_credits(state, student_id),
        instructions=get_instructions(state, student_id),
        tasks=get_tasks(state, student_id),
        recommendation=get_recommendation(state, student_id),
    )
    return overview


def get_student_level(state, student_id):
    return get_level(state, student_id)
