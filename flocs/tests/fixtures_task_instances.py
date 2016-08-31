import pytest
from flocs.entities import TaskInstance


@pytest.fixture
def task_instances_00():
    return {
        81: TaskInstance(
            task_instance_id=81,
            student_id=13,
            task_id=28,
            solved=False,
            given_up=False,
        ),
        14: TaskInstance(
            task_instance_id=14,
            student_id=37,
            task_id=67,
            solved=False,
            given_up=False,
        ),
    }


@pytest.fixture
def task_instances_01():
    return {
        81: TaskInstance(
            task_instance_id=81,
            student_id=13,
            task_id=28,
            solved=False,
            given_up=False,
        ),
        14: TaskInstance(
            task_instance_id=14,
            student_id=37,
            task_id=67,
            solved=False,
            given_up=False,
        ),
        27: TaskInstance(
            task_instance_id=27,
            student_id=37,
            task_id=28,
            solved=False,
            given_up=False,
        ),
    }


@pytest.fixture
def task_instances_02():
    return {
        81: TaskInstance(
            task_instance_id=81,
            student_id=13,
            task_id=28,
            solved=False,
            given_up=False,
        ),
        14: TaskInstance(
            task_instance_id=14,
            student_id=37,
            task_id=67,
            solved=True,
            given_up=False,
        ),
    }


@pytest.fixture
def task_instances_03():
    return {
        81: TaskInstance(
            task_instance_id=81,
            student_id=13,
            task_id=28,
            solved=False,
            given_up=False,
        ),
        14: TaskInstance(
            task_instance_id=14,
            student_id=37,
            task_id=67,
            solved=False,
            given_up=True,
        ),
    }


