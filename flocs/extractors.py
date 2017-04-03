""" Pure functions extracting information from the world state
"""
from collections import namedtuple
from operator import attrgetter
from flocs.entities import Student, Task, TaskSession, SeenInstruction, Level, Instruction
from flocs import recommendation


Recommendation = namedtuple('Recommendation', [
    'available',
    'task_id',
])


PracticeOverview = namedtuple('PracticeOverview', [
    'level',
    'credits',
    'active_credits',
    'instructions',
    'tasks',
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


def get_recommendation(state, student_id):
    task_id = recommendation.fixed_then_random(state, student_id)
    return Recommendation(available=True, task_id=task_id)


def get_practice_overview(state, student_id):
    student = state.entities[Student][student_id]
    overview = PracticeOverview(
        level=get_level(state, student_id).level_id,
        credits=student.credits,
        active_credits=get_active_credits(state, student_id),
        instructions=get_student_instructions(state, student_id),
        tasks=get_student_tasks(state, student_id),
    )
    return overview


def get_student_instructions(state, student_id):
    seen_instructions = state.entities[SeenInstruction].filter(student_id=student_id)
    # TODO: allow for student.seen_instructions
    instructions = state.entities[Instruction]
    student_instructions = [
        StudentInstruction(
            instruction_id=instruction_id,
            seen=seen_instructions.filter(instruction_id=instruction_id).exists(),
        )
        for instruction_id in instructions
    ]
    return student_instructions



def get_student_tasks(state, student_id):
    tasks = state.entities[Task]
    student_tasks = [
        StudentTask(
            task_id=task_id,
            solved=is_solved(state, student_id, task_id),
            time=get_time(state, student_id, task_id),
        )
        for task_id in tasks
    ]
    return student_tasks


def is_solved(state, student_id, task_id):
    solved_task_sessions = state.entities[TaskSession].filter(student_id=student_id, task_id=task_id, solved=True)
    return solved_task_sessions.exists()


def get_time(state, student_id, task_id):
    """ Best time if student has solved the task, otherwise just the last time
    """
    task_sessions = state.entities[TaskSession].filter(student_id=student_id, task_id=task_id)
    solved_task_sessions = task_sessions.filter(solved=True)
    if solved_task_sessions.exists():
        times = [ts.time_spent for ts in solved_task_sessions.values()]
        return min(times)
    last_task_session = task_sessions.order_by('time_end').last()
    return last_task_session.time_spent if last_task_session else None


def get_level(state, student_id):
    levels = state.entities[Level]
    if not levels:
        return Level(level_id=0, credits=0)
    student = state.entities[Student][student_id]
    level = max([level for level in levels.values() if student.credits - level.credits >= 0],
                key=attrgetter('credits'))
    return level


def get_active_credits(state, student_id):
    student = state.entities[Student][student_id]
    level = get_level(state, student_id)
    return student.credits - level.credits


def get_task_stats(state, task_id):
    raise NotImplementedError
