from flocs.actions import SolveTaskInstance, StartTaskInstance
from flocs.store import TaskInstance, reduce_task_instances
from flocs.store import TaskStats, reduce_tasks_stats


def test_reduce_task_instances():
    # TODO: make the test more readable using fixtures and test edge cases
    # TODO: what if task_instance_ids does not match idicies?!
    task_instances = (
        TaskInstance(
            task_instance_id=0,
            student_id=11,
            task_id=12,
            solved=False,
            given_up=False,
        ),
        TaskInstance(
            task_instance_id=1,
            student_id=13,
            task_id=14,
            solved=False,
            given_up=False,
        ),
        TaskInstance(
            task_instance_id=2,
            student_id=15,
            task_id=16,
            solved=False,
            given_up=False,
        ),
    )
    action = SolveTaskInstance(task_instance_id=1)
    next_task_instances = reduce_task_instances(action, task_instances)
    expected_next_task_instances = (
        task_instances[0],
        TaskInstance(
            task_instance_id=1,
            student_id=13,
            task_id=14,
            solved=True,
            given_up=False,
        ),
        task_instances[2],
    )
    assert next_task_instances == expected_next_task_instances


def test_reduce_tasks_stats():
    # TODO: make the test more readable using fixtures and test edge cases
    ANY = 0
    tasks_stats = (
        TaskStats(
            task_id=0,
            started_count=10,
            solved_count=20,
            given_up_count=30,
        ),
    )
    action = StartTaskInstance(task_id=0, student_id=ANY)
    next_tasks_stats = reduce_tasks_stats(action, tasks_stats)
    expected_tasks_stats = (
        TaskStats(
            task_id=0,
            started_count=11,
            solved_count=20,
            given_up_count=30,
        ),
    )
    assert next_tasks_stats == expected_tasks_stats
