""" Unit tests for extractors
"""
from flocs.extractors import get_level, get_unspent_credits
from flocs.state import default_static
from flocs.entities import Student


def test_get_level():
    student = Student(student_id=1, last_task_session_id=None, credits=15)
    state = default_static + student
    level = get_level(state, student_id=1)
    assert level.level_id == 3


def test_get_unspent_credits():
    student = Student(student_id=1, last_task_session_id=None, credits=15)
    state = default_static + student
    assert get_unspent_credits(state, student_id=1) == 6
