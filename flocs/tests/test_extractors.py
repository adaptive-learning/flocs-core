"""Unit tests for extractors
"""
from flocs import extractors
from flocs.entities import Task
from flocs.tests.fixtures_entities import ENTITIES
from flocs.tests.fixtures_states import STATES
from functools import partial
import random


def test_select_random_task():
    s3 = STATES['s3']
    tasks = s3.entities[Task]
    stud1_id = ENTITIES['stud1'].student_id
    random.seed(s3.context['randomness'])
    task_ids = list(tasks.keys())
    expected_task = random.choice(task_ids)
    selected_task = extractors.select_random_task(s3, stud1_id)
    assert expected_task == selected_task


def test_select_task_in_fixed_order():
    stud1 = ENTITIES['stud1']
    s3 = STATES['s3']
    order = [55, 28, 67]
    select_task_in_fixed_order_a = partial(extractors.general_select_task_in_fixed_order, order=order)
    selected_task_id = select_task_in_fixed_order_a(s3, stud1.student_id)
    assert selected_task_id == 67


def test_select_task_in_fixed_order_last_task():
    stud1 = ENTITIES['stud1']
    s3 = STATES['s3']
    order = [55, 67, 28]
    message = 'no exception raised'
    select_task_in_fixed_order_a = partial(extractors.general_select_task_in_fixed_order, order=order)
    try:
        select_task_in_fixed_order_a(s3, stud1.student_id)
    except ValueError as ve:
        message = '{0}'.format(ve)
    assert message == 'last task reached, there is no next task'
