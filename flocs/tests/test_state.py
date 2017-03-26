""" Unit tests for flocs.state
"""
from collections import namedtuple
from flocs import actions
from flocs.context import StaticContext
from flocs.entities import Action, Student, TaskSession
from flocs.entity_map import EntityMap
from flocs.state import empty, State, reduce_entity_map, reduce_state


# simple entity class for testing and a few instances
Entity = namedtuple('Entity', ['entity_id', 'a'])
e1 = Entity(entity_id='i', a=1)
e2 = Entity(entity_id='j', a=2)
e3 = Entity(entity_id='k', a=3)


def test_add_context():
    state = empty + StaticContext(time=1, randomness=2)
    assert state.time == 1
    assert state.randomness == 2


def test_add_entity():
    state = empty + e1
    assert set(state.entities[Entity].values()) == {e1}


def test_add_multiple_entities():
    state = empty + e1 + e2
    assert set(state.entities[Entity].values()) == {e1, e2}


def test_add_entities_dont_modify_original_state():
    state_1 = empty + e1
    state_2 = state_1 + e2
    assert Entity not in empty.entities
    assert set(state_1.entities[Entity].values()) == {e1}
    assert set(state_2.entities[Entity].values()) == {e1, e2}


def test_add_action():
    a1 = actions.create(type='create-student', data={'student-id': 20})
    state = empty + a1
    assert Entity not in empty.entities
    assert set(state.entities[Action].values()) == {a1}
    students = list(state.entities[Student].values())
    assert len(students) == 1
    assert students[0].student_id == 20


def test_add():
    state1 = empty + e1
    state2 = state1.add([e2, e3])
    assert set(state2.entities[Entity].values()) == {e1, e2, e3}


def test_build():
    state = State.build(e1, e2)
    assert set(state.entities[Entity].values()) == {e1, e2}


#def test_add_state():
#    state_a = State(entities=pmap({1: [11, 12]}))
#    state_b = State(entities=pmap({1: [11, 13], 2: [25, 26]}))
#    state_c = state_a + state_b
#    assert state_a == State(entities=pmap({1: [11, 12]}))
#    assert state_b == State(entities=pmap({1: [11, 13], 2: [25, 26]}))
#    assert state_c == State(entities=pmap({1: [11, 12, 13], 2: [25, 26]}))


def test_reduce_entity_map():
    task_sessions = EntityMap.from_list([
        TaskSession(task_session_id=14, student_id=37, task_id=67, solved=False, given_up=False)
    ])
    action = actions.create(type='solve-task', data={'task-session-id': 14})
    next_entity_map = reduce_entity_map(TaskSession, task_sessions, action)
    expected_entity_map = EntityMap.from_list([
        TaskSession(task_session_id=14, student_id=37, task_id=67, solved=True, given_up=False)
    ])
    assert next_entity_map == expected_entity_map


def test_reduce_state():
    a1 = actions.create(type='create-student', data={'student-id': 20})
    next_state = reduce_state(empty, a1)
    assert set(next_state.entities[Action].values()) == {a1}
    students = list(next_state.entities[Student].values())
    assert len(students) == 1
    assert students[0].student_id == 20
