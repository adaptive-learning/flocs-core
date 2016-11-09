"""Unit tests for state
"""

from flocs import state
from flocs.entities import Student, Task, TaskSession
from flocs.data.tasks import TASKS


def test_create_static_entities():
    created_entities = state.create_static_entities()
    expected_entities = {
        Student: {},
        Task: state.create_tasks_dict(),
        TaskSession: {},
    }
    assert created_entities == expected_entities


def test_create_tasks_dict():
    expected = {task.task_id: task for task in TASKS}
    created = state.create_tasks_dict()
    assert expected == created
