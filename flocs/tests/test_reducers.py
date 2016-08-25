from inspect import signature
from flocs.actions import ActionCreators
from flocs.entities import TaskStats
from flocs.reducers import reduce_task_instances, reduce_tasks_stats
from flocs.reducers import data_extracting
from flocs.tests.states import STATE_3, STATE_4

ANY_NUMBER = 0


# --------------------------------------------------------------------------


def test_data_extracting_signature():
    @data_extracting
    def subreducer(some_substate, a, c):
        pass
    assert tuple(signature(subreducer).parameters) == ('substate', 'data')


def test_data_extracting_correct_values():
    @data_extracting
    def subreducer(some_substate, a, c):
        return ('result', some_substate, a, c)
    result = subreducer(substate='S', data={'a': 1, 'b': 2, 'c': 3})
    assert result == ('result', 'S', 1, 3)


# --------------------------------------------------------------------------

def test_reduce_task_instances():
    action = ActionCreators.solve_task(task_instance_id=0)
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
    action = ActionCreators.start_task(task_id=0, task_instance_id=ANY_NUMBER, student_id=ANY_NUMBER)
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
