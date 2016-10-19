"""Unit tests for reducers
"""
from flocs import actions, reducers
from flocs.entities import Student, TaskInstance
from flocs.reducers import reduce_state, extracting_data_context, extract_parameters
from flocs.tests.fixtures_entities import ENTITIES, task_instances_dict
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
    students = {79: Student(student_id=79, last_task_instance=14)}
    next_students = reducers.create_student(students, student_id=37, last_task_instance=14)
    expected_students = {79: Student(student_id=79, last_task_instance=14), 37: Student(student_id=37, last_task_instance=14)}
    assert next_students == expected_students


def test_create_task_instance():
    ti3 = ENTITIES['ti3']
    next_task_instances = reducers.create_task_instance(
        task_instances=task_instances_dict('ti1', 'ti2'),
        student_id=ti3.student_id,
        task_id=ti3.task_id,
        task_instance_id=ti3.task_instance_id,
    )
    assert next_task_instances == task_instances_dict('ti1', 'ti2', 'ti3')


def test_solve_task_instance():
    next_task_instances = reducers.solve_task_instance(
        task_instances=task_instances_dict('ti1', 'ti2'),
        task_instance_id=ENTITIES['ti2'].task_instance_id,
    )
    assert next_task_instances == task_instances_dict('ti1', 'ti2s')


def test_give_up_task_instance():
    next_task_instances = reducers.give_up_task_instance(
        task_instances=task_instances_dict('ti1', 'ti2'),
        task_instance_id=ENTITIES['ti2'].task_instance_id,
    )
    assert next_task_instances == task_instances_dict('ti1', 'ti2g')


# ---------------------------------------------------------------------------


def test_reduce_entity():
    ti2 = ENTITIES['ti2']
    next_entity_dict = reducers.reduce_entity(
        TaskInstance,
        task_instances_dict('ti1', 'ti2'),
        action=actions.solve_task(task_instance_id=ti2.task_instance_id),
    )
    assert next_entity_dict == task_instances_dict('ti1', 'ti2s')


def test_reduce_entities():
    action = actions.solve_task(task_instance_id=14)
    next_entities = reducers.reduce_entities(STATES['s1'].entities, action)
    assert next_entities == STATES['s2'].entities


def test_reduce_state():
    action = actions.solve_task(task_instance_id=14).at(STATES['s1'])
    next_state = reduce_state(STATES['s1'], action)
    assert next_state == STATES['s2']
