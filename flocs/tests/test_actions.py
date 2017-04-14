""" Unit tests for flocs.actions
"""
from datetime import datetime
import pytest
from flocs import actions
from flocs.action_factory import DuplicateAction
from flocs.actions import StartSession, StartTask, SolveTask
from flocs.context import static, Context
from flocs.entities import Action, Session, TaskSession
from flocs.state import empty
from flocs import __version__
from .fixtures_entities import s1, t2


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
    session = Session(session_id=10, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    state = empty + session + Context(time=datetime(1, 1, 1, 0))
    with pytest.raises(DuplicateAction) as excinfo:
        StartSession(student_id=1).at(state)
    assert excinfo.value.action.data == {'session_id': 10, 'student_id': 1}


def test_not_discarding_start_session_action():
    session1 = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    session2 = Session(session_id=2, student_id=2, start=None, end=datetime(1, 1, 2, 0))
    state = empty + session1 + session2 + Context(time=datetime(1, 1, 2, 0), new_id=10)
    action = StartSession(student_id=1).at(state)
    assert action.data == {'session_id': 10, 'student_id': 1}


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


def test_discarding_start_task_action():
    """ StartTask should be discarded if the task was already started in the
        current session
    """
    state = empty + s1 + t2 + Context(time=datetime(1, 1, 1), new_id=7)
    state = state.reduce(StartTask(student_id=1, task_id=2))
    state += Context(time=datetime(1, 1, 1, 0, 1), new_id=14)
    with pytest.raises(DuplicateAction) as excinfo:
        StartTask(student_id=1, task_id=2).at(state)
    expected_data = {'student_id': 1, 'task_id': 2, 'task_session_id': 7, 'session_id': 7}
    assert excinfo.value.action.data == expected_data


def test_not_discarding_start_task_action():
    state = empty + s1 + t2 + Context(time=datetime(1, 1, 1))
    state = state.reduce(StartTask(student_id=1, task_id=2))
    state += Context(time=datetime(1, 1, 2), new_id=3)
    action = StartTask(student_id=1, task_id=2).at(state)
    assert action.data == {'student_id': 1, 'task_id': 2, 'task_session_id': 3, 'session_id': 3}


def test_create_solve_task_action():
    session = Session(session_id=58, student_id=22, start=0, end=datetime(1, 1, 1, 0))
    ts = TaskSession(task_session_id=35, student_id=22, task_id=2, start=0,
                     end=datetime(1, 1, 1, 0))
    state = empty + session + ts + Context(time=datetime(1, 1, 1, 0), new_id=4)
    action = SolveTask(task_session_id=35).at(state)
    expected_action = Action(
        action_id=4,
        type='solve-task',
        data={'task_session_id': 35, 'student_id': 22, 'task_id': 2, 'session_id': 58},
        time=datetime(1, 1, 1, 0),
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
