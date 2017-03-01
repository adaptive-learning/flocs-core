"""Entities objects for testing purposes
"""
from flocs.entities import Task, TaskSession, Student, TaskStats
from flocs.state import EntityMap


ENTITIES = {
    'ts1': TaskSession(
        task_session_id=81,
        student_id=13,
        task_id=28,
        solved=False,
        given_up=False,
    ),
    'ts2': TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        solved=False,
        given_up=False,
    ),
    'ts2s': TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        solved=True,
        given_up=False,
    ),
    'ts2g': TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        solved=False,
        given_up=True,
    ),
    'ts3': TaskSession(
        task_session_id=27,
        student_id=37,
        task_id=28,
        solved=False,
        given_up=False,
    ),
    'ts3s': TaskSession(
        task_session_id=27,
        student_id=37,
        task_id=28,
        solved=True,
        given_up=False,
    ),
    't1': Task(
        task_id=28,
        category_id=None,
        setting=None,
        solution=None,
    ),
    't2': Task(
        task_id=67,
        category_id=None,
        setting=None,
        solution=None,
    ),
    't3': Task(
        task_id=55,
        category_id=None,
        setting=None,
        solution=None,
    ),
    'stud1': Student(
        student_id=13,
        last_task_session_id=81
    ),
    'stud2': Student(
        student_id=37,
        last_task_session_id=14
    ),
    's_new': Student(
        student_id=48,
        last_task_session_id=None
    ),
    's_not_new': Student(
        student_id=48,
        last_task_session_id=14
    ),
    # unusual name of this fixture forced by function
    # update_last_task_session_id which upgrades a student
    # with a new student where =student_id= as a new key
    94: Student(
        student_id=94,
        last_task_session_id=None
    ),
    'stat1': TaskStats(
        task_stats_id=28,
        task_id=28,
        started_count=3,
        solved_count=1,
        given_up_count=1,
    ),
    'stat1st': TaskStats(
        task_stats_id=28,
        task_id=28,
        started_count=4,
        solved_count=1,
        given_up_count=1,
    ),
    'stat1so': TaskStats(
        task_stats_id=28,
        task_id=28,
        started_count=3,
        solved_count=2,
        given_up_count=1,
    ),
    'stat1g': TaskStats(
        task_stats_id=28,
        task_id=28,
        started_count=3,
        solved_count=1,
        given_up_count=2,
    ),
    'stat2': TaskStats(
        task_stats_id=67,
        task_id=67,
        started_count=5,
        solved_count=4,
        given_up_count=0,
    ),
}


# TODO: replace by single function entity_mapping_from_keys()
def task_sessions_dict(*keys):
    return EntityMap({ENTITIES[key].task_session_id: ENTITIES[key] for key in keys})


def tasks_dict(*keys):
    return EntityMap({ENTITIES[key].task_id: ENTITIES[key] for key in keys})


def students_dict(*keys):
    return EntityMap({ENTITIES[key].student_id: ENTITIES[key] for key in keys})

def task_stats_dict(*keys):
    return EntityMap({ENTITIES[key].task_id: ENTITIES[key] for key in keys})
