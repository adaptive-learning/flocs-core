""" Pure functions extracting information related to student from the world state
"""
from collections import namedtuple
from flocs.entities import Level
from flocs.extractors import is_solved, get_time, needed_credits_for_levels, get_needed_credits_for_level

StudentInstruction = namedtuple('StudentInstruction', [
    'instruction_id',
    'seen',
])

StudentTask = namedtuple('StudentTask', [
    'task_id',
    'solved',
    'time',
])


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


def get_student_level(state, student_id):
    if not state.levels:
        return Level(level_id=0, credits=0)
    student = state.students[student_id]
    level = Level(level_id=0, credits=0)
    for next_level, needed_credits in needed_credits_for_levels(state):
        if student.credits >= needed_credits:
            level = next_level
        else:
            return level
    return level


def get_active_credits(state, student_id):
    student = state.students[student_id]
    level = get_student_level(state, student_id)
    passive_credits = get_needed_credits_for_level(state, level.level_id)
    active_credits = student.credits - passive_credits
    return active_credits
