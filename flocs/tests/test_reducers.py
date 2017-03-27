""" Unit tests for reducers
"""
# pylint: disable=no-value-for-parameter, unused-argument

from flocs import actions, reducers
from flocs.actions import ActionType
from flocs.entities import Action, Student, TaskSession, SeenInstruction
from flocs.entity_map import EntityMap
from flocs.reducers import reducer, extract_parameters


def test_get():
    assert reducers.get(Student, ActionType.create_student) == reducers.create_student


def test_reducer_decorator_signature():
    @reducer(None, None)
    def subreducer(substate, arg1, arg2):
        pass
    assert extract_parameters(subreducer, skip=1) == ('action',)


def test_reduce_decorator_passing_data():
    @reducer(None, 't')
    def subreducer(substate, a, c, context):
        assert a == 1
        assert c == 3
        assert context.time == 10
        assert context.randomness == 20
        return substate
    action = Action(action_id=1, type='t', data={'a': 1, 'b': 2, 'c': 3},
                    time=10, randomness=20, version=30)
    em = EntityMap()
    result = subreducer(em, action)
    assert result is em


def test_extract_parameters():
    def tmp_function(students, student_id, last_task_session_id=0):
        pass
    fn = tmp_function
    parameters = extract_parameters(fn, skip=1)
    expected_parameters = ('student_id', 'last_task_session_id')
    assert parameters == expected_parameters


def test_create_student():
    # let
    s1 = Student(student_id=13, last_task_session_id=81, credits=10)
    students = EntityMap.from_list([s1])
    # then
    action = actions.create(type='create-student', data={'student-id': 37})
    next_students = reducers.create_student(students, action)
    # expect
    s2 = Student(student_id=37, last_task_session_id=None, credits=0)
    expected_students = EntityMap.from_list([s1, s2])
    assert next_students == expected_students


def test_update_last_task_session_id():
    students = EntityMap.from_list([
        Student(student_id=13, last_task_session_id=81, credits=0),
    ])
    action = actions.create(type='start-task',
                            data={'task-session-id': 92, 'student-id': 13, 'task-id': 20})
    next_students = reducers.update_last_task_session_id(students, action)
    expected_students = EntityMap.from_list([
        Student(student_id=13, last_task_session_id=92, credits=0),
    ])
    assert next_students == expected_students


def test_create_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28, solved=False, given_up=False)
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67, solved=False, given_up=False)
    task_sessions = EntityMap.from_list([ts1, ts2])
    action = actions.create(type='start-task',
                            data={'task-session-id': 92, 'student-id': 13, 'task-id': 50})
    next_task_sessions = reducers.create_task_session(task_sessions, action)
    expected_task_sessions = EntityMap.from_list([
        ts1, ts2,
        TaskSession(task_session_id=92, student_id=13, task_id=50, solved=False, given_up=False),
    ])
    assert next_task_sessions == expected_task_sessions


def test_solve_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28, solved=False, given_up=False)
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67, solved=False, given_up=False)
    task_sessions = EntityMap.from_list([ts1, ts2])
    action = actions.create(type='solve-task', data={'task-session-id': 14})
    next_task_sessions = reducers.solve_task_session(task_sessions, action)
    ts2s = TaskSession(task_session_id=14, student_id=37, task_id=67, solved=True, given_up=False)
    expected_task_sessions = EntityMap.from_list([ts1, ts2s])
    assert next_task_sessions == expected_task_sessions


def test_give_up_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28, solved=False, given_up=False)
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67, solved=False, given_up=False)
    task_sessions = EntityMap.from_list([ts1, ts2])
    action = actions.create(type='give-up-task', data={'task-session-id': 14})
    next_task_sessions = reducers.give_up_task_session(task_sessions, action)
    ts2g = TaskSession(task_session_id=14, student_id=37, task_id=67, solved=False, given_up=True)
    expected_task_sessions = EntityMap.from_list([ts1, ts2g])
    assert next_task_sessions == expected_task_sessions


def test_see_instruction():
    seen_instructions = EntityMap.from_list([
        SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2)
    ])
    action = actions.create(type='see-instruction',
                            data={'seen-instruction-id': 15, 'student-id': 1, 'instruction-id': 7})
    next_seen_instructions = reducers.create_or_update_seen_instruction(seen_instructions, action)
    expected_seen_instructions = EntityMap.from_list([
        SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2),
        SeenInstruction(seen_instruction_id=15, student_id=1, instruction_id=7),
    ])
    assert next_seen_instructions == expected_seen_instructions


def test_see_instruction_more_students():
    seen_instructions = EntityMap.from_list([
        SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2)
    ])
    action = actions.create(type='see-instruction',
                            data={'seen-instruction-id': 15, 'student-id': 8, 'instruction-id': 2})
    next_seen_instructions = reducers.create_or_update_seen_instruction(seen_instructions, action)
    expected_seen_instructions = EntityMap.from_list([
        SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2),
        SeenInstruction(seen_instruction_id=15, student_id=8, instruction_id=2),
    ])
    assert next_seen_instructions == expected_seen_instructions


def test_see_same_instruction_again():
    si = SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2)
    seen_instructions = EntityMap.from_list([si])
    action = actions.create(type='see-instruction',
                            data={'seen-instruction-id': 15, 'student-id': 1, 'instruction-id': 2})
    next_seen_instructions = reducers.create_or_update_seen_instruction(seen_instructions, action)
    assert next_seen_instructions == seen_instructions


def test_identity_defaultdict():
    initial_dict = {'a': 1}
    processed_dict = reducers.identity_defaultdict(initial_dict)
    assert processed_dict == initial_dict
    assert processed_dict['b']('S', 'a') == 'S'


def test_identity_reducer():
    state = {'x': [10, 20]}
    assert reducers.identity_reducer(state, 'action') == {'x': [10, 20]}
