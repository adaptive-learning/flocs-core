"""Unit tests for extractors
"""
from flocs import extractors
from flocs.tests.fixtures_entities import ENTITIES
from flocs.tests.fixtures_states import STATES
from functools import partial


def test_select_task_in_fixed_order():
    stud1 = ENTITIES['stud1']
    s3 = STATES['s3']
    order = [55, 28, 67]
    select_task_in_fixed_order_a = partial(extractors.general_select_task_in_fixed_order, order=order)
    selected_task_id = select_task_in_fixed_order_a(s3, stud1.student_id)
    assert selected_task_id == 67
