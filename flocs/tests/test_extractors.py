"""Unit tests for extractors
"""
from functools import partial, reduce
import random
import pytest
from flocs.extractors import select_random_task, general_select_task_in_fixed_order, select_task_fixed_then_random
from flocs.extractors import select_task_in_fixed_order
from flocs.reducers import reduce_state
from flocs.entities import Task, TaskSession, Student
from flocs.context import STATIC_CONTEXT
from flocs import actions
from flocs.tests.fixtures_entities import ENTITIES
from flocs.tests.fixtures_states import STATES


def test_select_random_task():
    s3 = STATES['s3']
    tasks = s3.entities[Task]
    stud1_id = ENTITIES['stud1'].student_id
    random.seed(s3.context['randomness'])
    task_ids = list(tasks.keys())
    expected_task = random.choice(task_ids)
    selected_task = select_random_task(s3, stud1_id)
    assert expected_task == selected_task


def test_general_select_task_in_fixed_order():
    state = STATES['s5']
    student = ENTITIES['stud2']
    select_task = partial(general_select_task_in_fixed_order, order=[28, 67, 55])
    selected_task_id = select_task(state, student.student_id)
    # The student solved tasks 28 and 67 (67 was in the last task session)
    assert selected_task_id == 55


def test_select_task_in_fixed_order_no_skipping():
    state = STATES['s5']
    student = ENTITIES['stud2']
    select_task = partial(general_select_task_in_fixed_order, order=[55, 67, 28])
    selected_task_id = select_task(state, student.student_id)
    assert selected_task_id == 55


def test_select_task_in_fixed_order_last_task():
    state = STATES['s5']
    stud1 = ENTITIES['stud2']
    message = 'no exception raised'
    select_task_in_fixed_order_a = partial(general_select_task_in_fixed_order, order=[28, 67])
    try:
        select_task_in_fixed_order_a(state, stud1.student_id)
    except ValueError as ve:
        message = '{0}'.format(ve)
    assert message == 'last task reached, there is no next task'


def test_select_same_task_until_solved():
    state = STATES['s4']
    student = ENTITIES['s_new']
    action1 = actions.start_task(
        student_id=student.student_id,
        task_id='t1')
    state = reduce_state(state, action1)
    select_task = partial(general_select_task_in_fixed_order, order=['t1', 't2'])
    selected_task_id = select_task(state, student.student_id)
    assert selected_task_id == 't1'
    action2 = actions.solve_task(
        task_session_id=action1.data['task_session_id'])
    state = reduce_state(state, action2)
    selected_task_id = select_task(state, student.student_id)
    assert selected_task_id == 't2'


def test_select_task_in_fixed_order():
    state = STATES['s4']
    student = ENTITIES['s_new']
    expected_order = [
        'one-step-forward',
        'diamond-on-right',
        'wormhole-demo',
        'shot',
        'ladder',
    ]
    for expected_task_id in expected_order:
        selected_task_id = select_task_in_fixed_order(state, student.student_id)
        assert selected_task_id == expected_task_id
        action1 = actions.start_task(
            student_id=student.student_id,
            task_id=selected_task_id)
        action2 = actions.solve_task(
            task_session_id=action1.data['task_session_id'])
        state = reduce(reduce_state, [action1, action2], state)
    # all tasks solved
    with pytest.raises(ValueError):
        select_task_in_fixed_order(state, student.student_id)


def test_select_task_fixed_then_random():
    state = STATES['s4']
    expected_order = [
        'one-step-forward',
        'diamond-on-right',
        'wormhole-demo',
        'shot',
        'ladder',
    ]
    for i in range(3 * len(state.entities[Task])):
        student = state.entities[Student][48]
        selected_task_id = select_task_fixed_then_random(
            state, student.student_id)
        if i < len(expected_order):
            assert selected_task_id == expected_order[i]
        elif i < len(state.entities[Task]):
            assert selected_task_id not in expected_order
            task_sessions_of_task = state.entities[TaskSession].filter(
                student_id=student.student_id,
                task_id=selected_task_id)
            if task_sessions_of_task:
                for task_session in task_sessions_of_task:
                    assert not task_session.solved
        else:
            task_sessions_of_task = state.entities[TaskSession].filter(
                student_id=student.student_id,
                task_id=selected_task_id)
            solved = False
            for task_session in task_sessions_of_task.values():
                if task_session.solved:
                    solved = True
            assert solved
            last_ts_id = student.last_task_session_id
            last_task_id = state.entities[TaskSession][last_ts_id].task_id
            assert selected_task_id != last_task_id
        action1 = actions.start_task(
            student_id=student.student_id,
            task_id=selected_task_id).at(state)
        action2 = actions.solve_task(
            task_session_id=action1.data['task_session_id']).at(state)
        state = reduce(reduce_state, [action1, action2], state)
