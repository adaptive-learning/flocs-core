from flocs import actions, reducers
from flocs.entities import Student, TaskInstance, TaskStats
from flocs.reducers import reduce_state, extracting_data_context, extract_parameters

# load pytest fixtures
from flocs.tests.fixtures_task_instances import *
from flocs.tests.fixtures_entities import *
from flocs.tests.fixtures_states import *


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


def test_create_student():
    students = {79: Student(student_id=79)}
    next_students = reducers.create_student(students, student_id=37)
    expected_students = {79: Student(student_id=79), 37: Student(student_id=37)}
    assert next_students == expected_students


def test_create_task_instance(task_instances_00, task_instances_01):
    next_task_instances = reducers.create_task_instance(
        task_instances_00,
        student_id=37,
        task_id=28,
        task_instance_id=27,
    )
    assert next_task_instances == task_instances_01


def test_solve_task_instance(task_instances_00, task_instances_02):
    next_task_instances = reducers.solve_task_instance(task_instances_00, task_instance_id=14)
    assert next_task_instances == task_instances_02


def test_give_up_task_instance(task_instances_00, task_instances_03):
    next_task_instances = reducers.give_up_task_instance(task_instances_00, task_instance_id=14)
    assert next_task_instances == task_instances_03


# ---------------------------------------------------------------------------


def test_reduce_entity(task_instances_00, task_instances_02):
    action = actions.solve_task(task_instance_id=14)
    next_entity_dict = reducers.reduce_entity(TaskInstance, task_instances_00, action)
    assert next_entity_dict == task_instances_02


def test_reduce_entities(entities_01, entities_02):
    action = actions.solve_task(task_instance_id=14)
    next_entities = reducers.reduce_entities(entities_01, action)
    assert next_entities == entities_02


def test_reduce_state(state_01, state_02):
    action = actions.solve_task(task_instance_id=14).at(state_01)
    next_state = reduce_state(state_01, action)
    assert next_state == state_02
