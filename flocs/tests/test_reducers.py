"""Unit tests for reducers
"""
from flocs import actions, reducers
from flocs.entities import Student, TaskSession
from flocs.reducers import reduce_state, extracting_data_context, extract_parameters
from flocs.tests.fixtures_entities import ENTITIES, task_sessions_dict
from flocs.tests.fixtures_states import STATES


def test_extracting_data_context_signature():
    @extracting_data_context
    def subreducer(dummy_substate, dummy_arg1, dummy_arg2):
        pass
    assert extract_parameters(subreducer, skip=1) == ('data', 'context')


def test_extracting_data_context_values_from_data():
    @extracting_data_context
    def subreducer(some_substate, a, c):
        return ('result', some_substate, a, c)
    result = subreducer('S', data={'a': 1, 'b': 2, 'c': 3}, context={})
    assert result == ('result', 'S', 1, 3)


# --------------------------------------------------------------------------


def test_create_student():
    students = {79: Student(student_id=79, last_task_session=14)}
    next_students = reducers.create_student(students, student_id=37, last_task_session=14)
    expected_students = {79: Student(student_id=79, last_task_session=14), 37: Student(student_id=37, last_task_session=14)}
    assert next_students == expected_students


def test_create_task_session():
    ts3 = ENTITIES['ts3']
    next_task_sessions = reducers.create_task_session(
        task_sessions=task_sessions_dict('ts1', 'ts2'),
        student_id=ts3.student_id,
        task_id=ts3.task_id,
        task_session_id=ts3.task_session_id,
    )
    assert next_task_sessions == task_sessions_dict('ts1', 'ts2', 'ts3')


def test_solve_task_session():
    next_task_sessions = reducers.solve_task_session(
        task_sessions=task_sessions_dict('ts1', 'ts2'),
        task_session_id=ENTITIES['ts2'].task_session_id,
    )
    assert next_task_sessions == task_sessions_dict('ts1', 'ts2s')


def test_give_up_task_session():
    next_task_sessions = reducers.give_up_task_session(
        task_sessions=task_sessions_dict('ts1', 'ts2'),
        task_session_id=ENTITIES['ts2'].task_session_id,
    )
    assert next_task_sessions == task_sessions_dict('ts1', 'ts2g')


# ---------------------------------------------------------------------------


def test_reduce_entity():
    ts2 = ENTITIES['ts2']
    next_entity_dict = reducers.reduce_entity(
        TaskSession,
        task_sessions_dict('ts1', 'ts2'),
        action=actions.solve_task(task_session_id=ts2.task_session_id),
    )
    assert next_entity_dict == task_sessions_dict('ts1', 'ts2s')


def test_reduce_entities():
    action = actions.solve_task(task_session_id=14)
    next_entities = reducers.reduce_entities(STATES['s1'].entities, action)
    assert next_entities == STATES['s2'].entities


def test_reduce_state():
    action = actions.solve_task(task_session_id=14).at(STATES['s1'])
    next_state = reduce_state(STATES['s1'], action)
    assert next_state == STATES['s2']
