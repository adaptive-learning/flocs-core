from inspect import signature
from flocs.actions import create_student, start_task, solve_task
from flocs.entities import TaskStats
from flocs.reducers import reduce_state, extracting_data_context, extract_parameters
from flocs.tests.states import STATE_3, STATE_4

ANY_NUMBER = 0


# --------------------------------------------------------------------------


def test_extracting_data_context_signature():
    @extracting_data_context
    def subreducer(some_substate, a, c):
        pass
    assert extract_parameters(subreducer, skip=1) == ('data', 'context')


def test_extracting_data_context_values_from_data():
    @extracting_data_context
    def subreducer(some_substate, a, c):
        return ('result', some_substate, a, c)
    result = subreducer('S', data={'a': 1, 'b': 2, 'c': 3}, context={})
    assert result == ('result', 'S', 1, 3)


# --------------------------------------------------------------------------
# TODO: test all subreducers, as well as whole state reducer and entity reducer

def test_reduce_solve_task_action():
    action = solve_task(task_instance_id=0)
    next_state = reduce_state(STATE_3, action)
    assert next_state == STATE_4


#def test_reduce_tasks_stats():
#    tasks_stats = {
#        0: TaskStats(
#            task_id=0,
#            started_count=10,
#            solved_count=20,
#            given_up_count=30,
#            ),
#        }
#    action = start_task(task_id=0, task_instance_id=ANY_NUMBER, student_id=ANY_NUMBER)
#    next_tasks_stats = reduce_tasks_stats(tasks_stats, action)
#    expected_tasks_stats = {
#        0: TaskStats(
#            task_id=0,
#            started_count=11,
#            solved_count=20,
#            given_up_count=30,
#            ),
#        }
#    assert next_tasks_stats == expected_tasks_stats
