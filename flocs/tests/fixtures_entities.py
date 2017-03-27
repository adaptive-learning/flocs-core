"""Entities objects for testing purposes
"""
from flocs.entities import Task, TaskSession, Student
from flocs.state import EntityMap

s1 = Student(student_id=1, last_task_session_id=None, credits=0)

t1 = Task(task_id=1, category_id=None, setting=None, solution=None)
t2 = Task(task_id=2, category_id=None, setting=None, solution=None)
t3 = Task(task_id=3, category_id=None, setting=None, solution=None)
t4 = Task(task_id=4, category_id=None, setting=None, solution=None)
t5 = Task(task_id=5, category_id=None, setting=None, solution=None)
t6 = Task(task_id=6, category_id=None, setting=None, solution=None)
t7 = Task(task_id=7, category_id=None, setting=None, solution=None)
t8 = Task(task_id=8, category_id=None, setting=None, solution=None)
t9 = Task(task_id=9, category_id=None, setting=None, solution=None)


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
        last_task_session_id=81,
        credits=15,
    ),
    'stud2': Student(
        student_id=37,
        last_task_session_id=14,
        credits=0,
    ),
    's_new': Student(
        student_id=48,
        last_task_session_id=None,
        credits=0,
    ),
    's_not_new': Student(
        student_id=48,
        last_task_session_id=14,
        credits=0,
    ),
    # unusual name of this fixture forced by function
    # update_last_task_session_id which upgrades a student
    # with a new student where =student_id= as a new key
    94: Student(
        student_id=94,
        last_task_session_id=None,
        credits=0,
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
