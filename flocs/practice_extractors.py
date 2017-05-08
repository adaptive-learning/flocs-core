from collections import namedtuple
from flocs.student_extractors import get_active_credits, get_student_instructions, get_student_tasks, get_student_level
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


def get_recommendation(state, student_id):
    task_id = recommendation.random_by_level(state, student_id)
    return Recommendation(available=True, task_id=task_id)


def get_practice_overview(state, student_id):
    student = state.students[student_id]
    overview = PracticeOverview(
        level=get_student_level(state, student_id).level_id,
        credits=student.credits,
        active_credits=get_active_credits(state, student_id),
        instructions=get_student_instructions(state, student_id),
        tasks=get_student_tasks(state, student_id),
        recommendation=get_recommendation(state, student_id),
    )
    return overview
