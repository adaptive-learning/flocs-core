""" Unit tests for flocs.actions
"""
from datetime import datetime
import pytest
from flocs import actions
from flocs.actions import StartSession
from flocs.context import static, Context
from flocs.entities import Action, Session
from flocs.state import empty
from flocs import __version__


def test_create():
    action = actions.create(type='nothing-happens', data={})
    expected_action = actions.NothingHappens()
    assert action == expected_action


def test_create_with_data():
    action = actions.create(type='start-task', data={'student-id': 145, 'task-id': 782})
    expected_action = actions.StartTask(student_id=145, task_id=782)
    assert action == expected_action


def test_create_nothing_happens_action():
    action = actions.NothingHappens().at(empty + static)
    expected_action = Action(
        action_id=0,
        type='nothing-happens',
        data={},
        time=static.default_time,
        randomness=0,
        version=__version__,
    )
    assert action == expected_action


def test_create_start_session_action():
    action = actions.StartSession().at(empty + static)
    expected_action = Action(
        action_id=0,
        type='start-session',
        data={'session_id': 0, 'student_id': 0},
        time=static.default_time,
        randomness=0,
        version=__version__,
    )
    assert action == expected_action


def test_discarding_start_session_action():
    session = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    state = empty + session + Context(time=datetime(1, 1, 1, 0))
    action = StartSession(student_id=1).at(state)
    assert action is None


def test_not_discarding_start_session_action():
    session1 = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    session2 = Session(session_id=2, student_id=2, start=None, end=datetime(1, 1, 2, 0))
    state = empty + session1 + session2 + Context(time=datetime(1, 1, 2, 0))
    action = StartSession(student_id=1).at(state)
    assert action is not None


def test_create_start_task_action():
    action = actions.StartTask(student_id=145, task_id=782).at(empty + static)
    expected_action = Action(
        action_id=0,
        type='start-task',
        data={'student_id': 145, 'task_id': 782, 'task_session_id': 0, 'session_id': 0},
        time=static.default_time,
        randomness=0,
        version=__version__,
    )
    assert action == expected_action


def test_create_solve_task_action():
    action = actions.SolveTask(task_session_id=201).at(empty + static)
    expected_action = Action(
        action_id=0,
        type='solve-task',
        data={'task_session_id': 201},
        time=static.default_time,
        randomness=0,
        version=__version__,
    )
    assert action == expected_action




def test_create_see_instruction_action():
    action = actions.SeeInstruction(student_id=745, instruction_id=23).at(empty + static)
    expected_action = Action(
        action_id=0,
        type='see-instruction',
        data={'seen_instruction_id': 0, 'student_id': 745, 'instruction_id': 23},
        time=static.default_time,
        randomness=0,
        version=__version__,
    )
    assert action == expected_action


def test_create_nonexistent_action():
    with pytest.raises(ValueError):
        actions.create(type='invalid-action-type', data={})


def test_create_action_missing_data():
    with pytest.raises(ValueError):
        actions.create(type='solve-task', data={})


def test_create_action_redundant_data():
    with pytest.raises(ValueError):
        actions.create(type='solve-task', data={'task-session-id': 34, 'redundant-field': 20})


def test_create_action_with_autofields_provided():
    action = actions.create(type='start-session', data={'student-id': 22}).at(empty + static)
    expected_action = Action(
        action_id=0,
        type='start-session',
        data={'session_id': 0, 'student_id': 22},
        time=static.default_time,
        randomness=0,
        version=__version__,
    )
    assert action == expected_action
