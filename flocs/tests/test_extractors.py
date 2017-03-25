"""Unit tests for extractors
"""
from functools import partial
import pytest
from flocs.extractors import select_random_task
from flocs.extractors import general_select_task_in_fixed_order
from flocs.extractors import select_task_in_fixed_order
from flocs.extractors import select_task_fixed_then_random
from flocs.extractors import get_level, get_unspent_credits
from flocs.context import StaticContext
from flocs.state import State, default_static
from flocs.entities import Task, TaskSession, Student
from flocs.tests.fixtures_entities import s1
from flocs.tests.fixtures_entities import t2, t5, t9


def test_select_random_task():
    state_a = State.build(StaticContext(randomness=0), s1, t2, t5, t9)
    state_b = State.build(StaticContext(randomness=1), s1, t2, t5, t9)
    task_a = select_random_task(state_a, student_id=1)
    task_b = select_random_task(state_b, student_id=1)
    assert task_a in {2, 5, 9}
    assert task_b in {2, 5, 9}
    assert task_a != task_b  # if equal, change randomness seeds


def test_general_select_task_in_fixed_order():
    state = State.build(t2, t5, t9, s1)
    state += TaskSession(task_session_id=1, student_id=1, task_id=5, solved=True, given_up=False)
    select_task = partial(general_select_task_in_fixed_order, order=[5, 9, 2])
    selected_task_id = select_task(state, student_id=1)
    assert selected_task_id == 9


def test_select_task_in_fixed_order_no_skipping():
    state = State.build(t2, t5, t9, s1)
    state += TaskSession(task_session_id=1, student_id=1, task_id=9, solved=True, given_up=False)
    select_task = partial(general_select_task_in_fixed_order, order=[5, 9, 2])
    selected_task_id = select_task(state, student_id=1)
    assert selected_task_id == 5


def test_select_task_in_fixed_order_last_task():
    state = State.build(t2, t5, s1)
    state += TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, given_up=False)
    state += TaskSession(task_session_id=2, student_id=1, task_id=5, solved=True, given_up=False)
    select_task = partial(general_select_task_in_fixed_order, order=[2, 5])
    with pytest.raises(ValueError):
        select_task(state, student_id=1)


def test_select_same_task_until_solved():
    state = State.build(t2, t5, s1)
    select_task = partial(general_select_task_in_fixed_order, order=[2, 5])
    assert select_task(state, student_id=1) == 2
    state += TaskSession(task_session_id=1, student_id=1, task_id=2, solved=False, given_up=False)
    assert select_task(state, student_id=1) == 2
    state += TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, given_up=False)
    assert select_task(state, student_id=1) == 5


def test_select_task_in_fixed_order():
    state = default_static + s1
    state += TaskSession(task_session_id=1, student_id=1, task_id='one-step-forward',
                         solved=True, given_up=False)
    assert select_task_in_fixed_order(state, student_id=1) == 'diamond-on-right'


def test_select_task_fixed_then_random():
    state = default_static + s1
    unsolved = {task_id for task_id in state.entities[Task]}
    m = len(state.entities[Task])
    for k in range(m):
        next_task = select_task_fixed_then_random(state, student_id=1)
        assert next_task in unsolved
        unsolved.discard(next_task)
        state += TaskSession(task_session_id=k, student_id=1, task_id=next_task,
                             solved=True, given_up=False)
        state += Student(student_id=1, last_task_session_id=k, credits=0)

    # after all tasks were solved, it can pick any task, but should avoid the
    # task which was just solved
    last_task = next_task
    for k in range(m, 2*m):
        next_task = select_task_fixed_then_random(state, student_id=1)
        assert next_task != last_task
        last_task = next_task
        state += TaskSession(task_session_id=k, student_id=1, task_id=next_task,
                             solved=True, given_up=False)
        state += Student(student_id=1, last_task_session_id=k, credits=0)


def test_get_level():
    student = Student(student_id=1, last_task_session_id=None, credits=15)
    state = default_static + student
    level = get_level(state, student_id=1)
    assert level.level_id == 3


def test_get_unspent_credits():
    student = Student(student_id=1, last_task_session_id=None, credits=15)
    state = default_static + student
    assert get_unspent_credits(state, student_id=1) == 6
