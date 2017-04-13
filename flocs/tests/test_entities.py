""" Unit tests for entities
"""

from datetime import datetime, timedelta
from flocs.entities import TaskSession


def test_task_session_defaults():
    task_session = TaskSession(task_id=3, student_id=4)
    assert task_session.solved == False
    assert task_session.given_up == False


def test_task_session_spent_time():
    task_session = TaskSession(
        start=datetime(2017, 1, 10, 5, 30, 20),
        end=datetime(2017, 1, 10, 5, 31, 10),
    )
    assert task_session.time_spent == timedelta(seconds=50)
