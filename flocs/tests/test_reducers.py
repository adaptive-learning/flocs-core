"""Unit tests for reducers
"""
from flocs import actions, reducers
from flocs.entities import Student, TaskSession
from flocs.reducers import reduce_state, extracting_data_context, extract_parameters
from flocs.state import EntityMap
from flocs.tests.fixtures_entities import ENTITIES, task_sessions_dict, task_stats_dict
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


def test_extract_parameters():
    def tmp_function(students, student_id, last_task_session_id=0):
        pass
    fn = tmp_function
    parameters = reducers.extract_parameters(fn, skip=1)
    expected_parameters = ('student_id', 'last_task_session_id')
    assert parameters == expected_parameters


# --------------------------------------------------------------------------


def test_identity_defaultdict():
    def tmp_function():
        return 5
    initial_dict = {'a': 1}
    processed_dict = reducers.identity_defaultdict(initial_dict)
    assert processed_dict == initial_dict
    assert processed_dict['b'](tmp_function) == tmp_function


def test_identity_reducer():
    state = STATES['s3']
    assert reducers.identity_reducer(state) == state


# --------------------------------------------------------------------------


def test_create_student():
    students = EntityMap.from_list([
        Student(student_id=13, last_task_session_id=81)
    ])
    next_students = reducers.create_student(students, student_id=37)
    expected_students = EntityMap.from_list([
        Student(student_id=13, last_task_session_id=81),
        Student(student_id=37, last_task_session_id=None)
    ])
    assert next_students == expected_students


def test_update_last_task_session_id():
    s3 = STATES['s3']
    stud = ENTITIES[94]
    new_students = reducers.update_last_task_session_id(s3.entities[Student], 'new_ts_id', stud.student_id, 'some_task_id')
    assert new_students[stud.student_id].last_task_session_id == 'new_ts_id'


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


def test_reduce_entities_last_ts_id_updating():
    action = actions.start_task(student_id=48, task_id=67, task_session_id=14)
    next_entities = reducers.reduce_entities(STATES['s4'].entities, action)
    assert next_entities[Student][48] == ENTITIES['s_not_new']


def test_reduce_state():
    action = actions.solve_task(task_session_id=14).at(STATES['s1'])
    next_state = reduce_state(STATES['s1'], action)
    assert next_state == STATES['s2']


# ---------------------------------------------------------------------------


def test_increase_started_count():
    stats = task_stats_dict('stat1', 'stat2')
    new_stats = reducers.increase_started_count(stats=stats, task_id=28)
    assert new_stats == task_stats_dict('stat1st', 'stat2')


def test_increase_solved_count():
    stats = task_stats_dict('stat1', 'stat2')
    new_stats = reducers.increase_solved_count(stats=stats, task_id=28)
    assert new_stats == task_stats_dict('stat1so', 'stat2')


def test_increase_given_up_count():
    stats = task_stats_dict('stat1', 'stat2')
    new_stats = reducers.increase_given_up_count(stats=stats, task_id=28)
    assert new_stats == task_stats_dict('stat1g', 'stat2')
