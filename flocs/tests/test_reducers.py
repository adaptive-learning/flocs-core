""" Unit tests for reducers
"""
# pylint: disable=no-value-for-parameter, unused-argument

from flocs import reducers
from flocs.actions import ActionType, StartSession, StartTask, SolveTask, SeeInstruction
from flocs.context import Context
from flocs.entities import Action, Student, TaskSession, SeenInstruction, Session
from flocs.entity_map import EntityMap
from flocs.reducers import reducer, extract_parameters
from flocs.state import empty, State
from .fixtures_entities import s1


def test_get():
    assert reducers.get(Student, ActionType.start_session) == reducers.create_student_if_new


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


def test_create_student_if_new():
    state = empty + s1
    next_state = state.reduce(StartSession(student_id=37))
    s2 = Student(student_id=37, last_task_session_id=None, credits=0)
    assert next_state.students == EntityMap.from_list([s1, s2])


def test_update_last_task_session_id():
    student = Student(student_id=13, last_task_session_id=81, credits=0)
    session = Session(session_id=2, student_id=13, start_time=0, end_time=5)
    state = State() + student + session + Context(new_id=92)
    next_state = state.reduce(StartTask(student_id=13, task_id=50))
    updated_student = student._replace(last_task_session_id=92)
    assert next_state.students == EntityMap.from_list([updated_student])


def test_create_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28)
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67)
    session = Session(session_id=2, student_id=13, start_time=0, end_time=5)
    state = State() + session +  ts1 + ts2 + Context(time=7, new_id=92)
    next_state = state.reduce(StartTask(student_id=13, task_id=50))
    ts3 = TaskSession(task_session_id=92, student_id=13, task_id=50, time_start=7, time_end=7)
    expected_task_sessions = EntityMap.from_list([ts1, ts2, ts3])
    assert next_state.task_sessions == expected_task_sessions


def test_solve_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28, time_start=10, time_end=20)
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67, time_start=30, time_end=40)
    state = empty + ts1 + ts2
    next_state = state.reduce(SolveTask(task_session_id=14))
    ts2s = ts2._replace(solved=True)
    assert next_state.task_sessions == EntityMap.from_list([ts1, ts2s])


def test_see_instruction():
    si1 = SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2)
    state = empty + si1 + Context(new_id=15)
    next_state = state.reduce(SeeInstruction(student_id=1, instruction_id=7))
    si2 = SeenInstruction(seen_instruction_id=15, student_id=1, instruction_id=7)
    assert next_state.seen_instructions == EntityMap.from_list([si1, si2])


def test_see_instruction_more_students():
    si1 = SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2)
    state = empty + si1 + Context(new_id=15)
    next_state = state.reduce(SeeInstruction(student_id=8, instruction_id=2))
    si2 = SeenInstruction(seen_instruction_id=15, student_id=8, instruction_id=2)
    assert next_state.seen_instructions == EntityMap.from_list([si1, si2])


def test_see_same_instruction_again():
    si1 = SeenInstruction(seen_instruction_id=10, student_id=1, instruction_id=2)
    state = empty + si1 + Context(new_id=15)
    next_state = state.reduce(SeeInstruction(student_id=1, instruction_id=2))
    assert next_state.seen_instructions == EntityMap.from_list([si1])


def test_identity_defaultdict():
    initial_dict = {'a': 1}
    processed_dict = reducers.identity_defaultdict(initial_dict)
    assert processed_dict == initial_dict
    assert processed_dict['b']('S', 'a') == 'S'


def test_identity_reducer():
    state = {'x': [10, 20]}
    assert reducers.identity_reducer(state, 'action') == {'x': [10, 20]}
