"""Unit tests for extractors
"""
from functools import partial
import random
import pytest
from flocs.extractors import select_random_task, general_select_task_in_fixed_order
from flocs.extractors import select_task_in_fixed_order
from flocs.reducers import ENTITY_REDUCERS, reduce_state
from flocs.entities import Task, Student
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
    stud1 = ENTITIES['stud1']
    s3 = STATES['s3']
    order = [55, 28, 67]
    select_task_in_fixed_order_a = partial(general_select_task_in_fixed_order, order=order)
    selected_task_id = select_task_in_fixed_order_a(s3, stud1.student_id)
    assert selected_task_id == 67


def test_select_task_in_fixed_order_last_task():
    stud1 = ENTITIES['stud1']
    s3 = STATES['s3']
    order = [55, 67, 28]
    message = 'no exception raised'
    select_task_in_fixed_order_a = partial(general_select_task_in_fixed_order, order=order)
    try:
        select_task_in_fixed_order_a(s3, stud1.student_id)
    except ValueError as ve:
        message = '{0}'.format(ve)
    assert message == 'last task reached, there is no next task'


def test_select_task_in_fixed_order_changing_last_task_session():
    s3 = STATES['s3']
    stud = ENTITIES[94]
    order = ['t1', 't2', 't3']
    select_task_in_fixed_order_a = partial(general_select_task_in_fixed_order, order=order)
    first_selected_task_id = select_task_in_fixed_order_a(s3, stud.student_id)

    action = actions.start_task(student_id=stud.student_id,
                                task_id=first_selected_task_id,
                                task_session_id=42)
    s3_1 = reduce_state(s3, action)

    updated_stud = ENTITY_REDUCERS[Student][action.type](students=s3_1.entities[Student],
                                                         task_session_id=42,
                                                         student_id=stud.student_id,
                                                         task_id=first_selected_task_id,
                                                         )[stud.student_id]

    second_selected_task_id = select_task_in_fixed_order_a(s3_1, updated_stud.student_id)
    assert second_selected_task_id == 't2'


def test_select_task_in_fixed_order():
    state = STATES['s4']
    student = ENTITIES['s_new']
    expected_order = [
        'one-step-forward',
        'three-steps-forward',
        'turning-left',
        'turning-right-and-left',
        'diamond-on-right',
        'shot',
        'shooting',
        'zig-zag',
        'ladder',
        'on-yellow-to-left',
    ]
    for expected_task_id in expected_order:
        selected_task_id = select_task_in_fixed_order(state, student.student_id)
        assert selected_task_id == expected_task_id
        action = actions.start_task(
            student_id=student.student_id,
            task_id=selected_task_id)
        # the student should also solve task, not only start...
        state = reduce_state(state, action)
    # all tasks solved
    with pytest.raises(ValueError):
        select_task_in_fixed_order(state, student.student_id)
