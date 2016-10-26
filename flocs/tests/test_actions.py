"""Unit tests for flocs.actions
"""
from flocs import actions
from flocs.actions import Action
from flocs.state import State
from flocs.meta import META


def test_create_student():
    action = actions.create_student(student_id=17)
    expected_action = Action(
        type='create_student',
        data={'student_id': 17},
        context=None,
        meta=META,
    )
    assert action == expected_action


def test_create_student_at_state():
    state = State(entities='E', context='C', meta='M')
    action = actions.create_student(student_id=17).at(state)
    expected_action = Action(
        type='create_student',
        data={'student_id': 17},
        context='C',
        meta=META,
    )
    assert action == expected_action


def test_create_student_without_id(monkeypatch):
    monkeypatch.setattr('flocs.context.uuid4', lambda: 974)
    action = actions.create_student()
    expected_action = Action(
        type='create_student',
        data={'student_id': 974},
        context=None,
        meta=META,
    )
    assert action == expected_action


def test_start_task():
    action = actions.start_task(student_id=145, task_id=782, task_session_id=381)
    expected_action = Action(
        type='start_task',
        data={'student_id': 145, 'task_id': 782, 'task_session_id': 381},
        context=None,
        meta=META,
    )
    assert action == expected_action


def test_solve_task():
    action = actions.solve_task(task_session_id=651)
    expected_action = Action(
        type='solve_task',
        data={'task_session_id': 651},
        context=None,
        meta=META,
    )
    assert action == expected_action


def test_give_up_task():
    action = actions.give_up_task(task_session_id=798)
    expected_action = Action(
        type='give_up_task',
        data={'task_session_id': 798},
        context=None,
        meta=META,
    )
    assert action == expected_action
