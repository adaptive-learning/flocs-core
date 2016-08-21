from flocs.actions import StartTask, SolveTask
from flocs.entities import TaskStats
from flocs.reducers import reduce_task_instances, reduce_tasks_stats
from flocs.tests.states import STATE_3, STATE_4

ANY_NUMBER = 0

def test_reduce_task_instances():
    action = SolveTask(task_instance_id=0)
    task_instances = STATE_3['entities.task_instances']
    next_task_instances = reduce_task_instances(task_instances, action)
    expected_next_task_instances = STATE_4['entities.task_instances']
    assert next_task_instances == expected_next_task_instances


def test_reduce_tasks_stats():
    tasks_stats = {
        0: TaskStats(
            task_id=0,
            started_count=10,
            solved_count=20,
            given_up_count=30,
            ),
        }
    action = StartTask(task_id=0, task_instance_id=ANY_NUMBER, student_id=ANY_NUMBER)
    next_tasks_stats = reduce_tasks_stats(tasks_stats, action)
    expected_tasks_stats = {
        0: TaskStats(
            task_id=0,
            started_count=11,
            solved_count=20,
            given_up_count=30,
            ),
        }
    assert next_tasks_stats == expected_tasks_stats
