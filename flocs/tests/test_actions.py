""" Unit tests for flocs.actions
"""
import pytest
from flocs import actions
from flocs.context import StaticContext
from flocs.entities import Action
from flocs import __version__


def test_create_nothing_happens_action():
    action = actions.create(
        type='nothing-happens',
        data={},
        context=StaticContext())
    expected_action = Action(
        action_id=0,
        type='nothing-happens',
        data={},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
        version=__version__,
    )
    assert action == expected_action


def test_create_create_student_action():
    action = actions.create(
        type='create-student',
        data={},
        context=StaticContext())
    expected_action = Action(
        action_id=1,
        type='create-student',
        data={'student_id': 0},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
        version=__version__,
    )
    assert action == expected_action


def test_create_start_task_action():
    action = actions.create(
        type='start-task',
        data={'student-id': 145, 'task-id': 782},
        context=StaticContext())
    expected_action = Action(
        action_id=1,
        type='start-task',
        data={'student_id': 145, 'task_id': 782, 'task_session_id': 0},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
        version=__version__,
    )
    assert action == expected_action


def test_create_solve_task_action():
    action = actions.create(
        type='solve-task',
        data={'task-session-id': 201},
        context=StaticContext())
    expected_action = Action(
        action_id=0,
        type='solve-task',
        data={'task_session_id': 201},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
        version=__version__,
    )
    assert action == expected_action


def test_create_give_up_task_action():
    action = actions.create(
        type='give-up-task',
        data={'task-session-id': 201},
        context=StaticContext())
    expected_action = Action(
        action_id=0,
        type='give-up-task',
        data={'task_session_id': 201},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
        version=__version__,
    )
    assert action == expected_action


def test_create_see_instruction_action():
    action = actions.create(
        type='see-instruction',
        data={'student-id': 745, 'instruction-id': 23},
        context=StaticContext())
    expected_action = Action(
        action_id=1,
        type='see-instruction',
        data={'seen_instruction_id': 0, 'student_id': 745, 'instruction_id': 23},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
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
    action = actions.create(
        type='create-student',
        data={'student-id': 22},
        context=StaticContext())
    expected_action = Action(
        action_id=0,
        type='create-student',
        data={'student_id': 22},
        time=StaticContext.fixed_time,
        randomness=StaticContext.fixed_randomness,
        version=__version__,
    )
    assert action == expected_action
