"""Unit tests for extractors
"""
from flocs import extractors
from flocs.tests.fixtures_entities import ENTITIES
from flocs.tests.fixtures_states import STATES


def test_select_task_in_fixed_order():
    stud1 = ENTITIES['stud1']
    selected_task_id = extractors.select_task_in_fixed_order(STATES['s3'], stud1.student_id)
    assert selected_task_id == 67
