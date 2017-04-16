""" Unit tests of recommendation strategies
"""
from functools import partial
import pytest
from flocs import recommendation
from flocs.context import Context
from flocs.entities import TaskSession, Student
from flocs.state import State, empty, default
from .fixtures_entities import s1, t2, t3, t5, t9


def test_randomly():
    state_a = State.build(Context(randomness=0), s1, t2, t5, t9)
    state_b = State.build(Context(randomness=1), s1, t2, t5, t9)
    task_a = recommendation.randomly(state_a, student_id=1)
    task_b = recommendation.randomly(state_b, student_id=1)
    assert task_a in {2, 5, 9}
    assert task_b in {2, 5, 9}
    assert task_a != task_b  # if equal, change randomness seeds


def test_fixed_order():
    state = State.build(t2, t5, t9, s1)
    state += TaskSession(task_session_id=1, student_id=1, task_id=5, solved=True, given_up=False)
    select_task = partial(recommendation.fixed_order, order=[5, 9, 2])
    selected_task_id = select_task(state, student_id=1)
    assert selected_task_id == 9


def test_select_task_in_fixed_order_no_skipping():
    state = State.build(t2, t5, t9, s1)
    state += TaskSession(task_session_id=1, student_id=1, task_id=9, solved=True, given_up=False)
    select_task = partial(recommendation.fixed_order, order=[5, 9, 2])
    selected_task_id = select_task(state, student_id=1)
    assert selected_task_id == 5


def test_select_task_in_fixed_order_last_task():
    state = State.build(t2, t5, s1)
    state += TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, given_up=False)
    state += TaskSession(task_session_id=2, student_id=1, task_id=5, solved=True, given_up=False)
    select_task = partial(recommendation.fixed_order, order=[2, 5])
    with pytest.raises(ValueError):
        select_task(state, student_id=1)


def test_select_same_task_until_solved():
    state = State.build(t2, t5, s1)
    select_task = partial(recommendation.fixed_order, order=[2, 5])
    assert select_task(state, student_id=1) == 2
    state += TaskSession(task_session_id=1, student_id=1, task_id=2, solved=False, given_up=False)
    assert select_task(state, student_id=1) == 2
    state += TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, given_up=False)
    assert select_task(state, student_id=1) == 5


def test_default_fixed_order():
    state = default + s1
    state += TaskSession(task_session_id=1, student_id=1, task_id='one-step-forward',
                         solved=True, given_up=False)
    assert recommendation.fixed_order(state, student_id=1) == 'diamond-on-right'


def test_fixed_then_random():
    state = default + s1
    unsolved = {task_id for task_id in state.tasks}
    m = len(state.tasks)
    for k in range(m):
        next_task = recommendation.fixed_then_random(state, student_id=1)
        assert next_task in unsolved
        unsolved.discard(next_task)
        state += TaskSession(task_session_id=k, student_id=1, task_id=next_task,
                             solved=True, given_up=False, end=k)
        state += Student(student_id=1, credits=0)

    # after all tasks were solved, it can pick any task, but should avoid the
    # task which was just solved
    last_task = next_task
    for k in range(m, 2*m):
        next_task = recommendation.fixed_then_random(state, student_id=1)
        assert next_task != last_task
        last_task = next_task
        state += TaskSession(task_session_id=k, student_id=1, task_id=next_task,
                             solved=True, given_up=False, end=k)
        state += Student(student_id=1, credits=0)


def test_multicriteria_single_task():
    state = empty + s1 + t3
    task_id = recommendation.multicriteria(state, student_id=1, criteria=[])
    assert task_id == 3


def test_multicriteria():
    state = empty + s1 + t2 + t3
    f1 = lambda w, s, t: s + t
    f2 = lambda w, s, t: s - t
    criteria_a = [recommendation.Criterion(0.7, f1), recommendation.Criterion(0.3, f2)]
    criteria_b = [recommendation.Criterion(0.3, f1), recommendation.Criterion(0.7, f2)]
    assert recommendation.multicriteria(state, student_id=1, criteria=criteria_a) == 3
    assert recommendation.multicriteria(state, student_id=1, criteria=criteria_b) == 2
