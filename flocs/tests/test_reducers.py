""" Unit tests for reducers
"""
# pylint: disable=no-value-for-parameter, unused-argument

from datetime import datetime
from flocs import reducers
from flocs.actions import ActionType
from flocs.actions import StartSession, StartTask, SolveTask, SeeInstruction
from flocs.actions import RunProgram, EditProgram
from flocs.context import Context
from flocs.entities import Action, Student, TaskSession, SeenInstruction, Session, ProgramSnapshot
from flocs.entity_map import EntityMap
from flocs.reducers import reducer, extract_parameters
from flocs.state import empty, State
from .fixtures_entities import s1, t2


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
    def tmp_function(students, student_id):
        pass
    fn = tmp_function
    parameters = extract_parameters(fn, skip=1)
    expected_parameters = ('student_id',)
    assert parameters == expected_parameters


def test_create_student_if_new():
    state = empty + s1
    next_state = state.reduce(StartSession(student_id=37))
    s2 = Student(student_id=37, credits=0)
    assert next_state.students == EntityMap.from_list([s1, s2])


def test_start_task_creating_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28)
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67)
    state = empty + s1 + t2 + ts1 + ts2 + Context(time=7, new_id=92)
    next_state = state.reduce(StartTask(student_id=1, task_id=2))
    ts3 = TaskSession(task_session_id=92, student_id=1, task_id=2, start=7, end=7)
    expected_task_sessions = EntityMap.from_list([ts1, ts2, ts3])
    assert next_state.task_sessions == expected_task_sessions


def test_start_task_creating_first_session():
    state = empty + s1 + t2 + Context(time=datetime(1, 1, 2, 0), new_id=92)
    next_state = state.reduce(StartTask(student_id=1, task_id=2))
    session = Session(session_id=92, student_id=1,
                      start=datetime(1, 1, 2, 0), end=datetime(1, 1, 2, 0))
    expected_sessions = EntityMap.from_list([session])
    assert next_state.sessions == expected_sessions


def test_start_task_creating_new_session():
    session1 = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    state = empty + s1 + t2 + session1 + Context(time=datetime(1, 1, 2, 0), new_id=92)
    next_state = state.reduce(StartTask(student_id=1, task_id=2))
    session2 = Session(session_id=92, student_id=1,
                       start=datetime(1, 1, 2, 0), end=datetime(1, 1, 2, 0))
    expected_sessions = EntityMap.from_list([session1, session2])
    assert next_state.sessions == expected_sessions


def test_start_task_not_creating_session():
    session1 = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    state = empty + s1 + t2 + session1 + Context(time=datetime(1, 1, 1, 0), new_id=92)
    next_state = state.reduce(StartTask(student_id=1, task_id=2))
    expected_sessions = EntityMap.from_list([session1])
    assert next_state.sessions == expected_sessions


def test_solve_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28,
                      start=datetime(1, 1, 1, 10), end=datetime(1, 1, 1, 11))
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67,
                      start=datetime(1, 1, 1, 12), end=datetime(1, 1, 1, 12))
    state = empty + ts1 + ts2 + Context(time=datetime(1, 1, 1, 13))
    next_state = state.reduce(SolveTask(task_session_id=14))
    ts2s = ts2._replace(solved=True, end=datetime(1, 1, 1, 13))
    assert next_state.task_sessions == EntityMap.from_list([ts1, ts2s])


def test_solve_task_updating_session():
    session = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    ts = TaskSession(task_session_id=21, student_id=1, task_id=2,
                     start=datetime(1, 1, 1, 0), end=datetime(1, 1, 1, 0))
    state = empty + s1 + t2 + ts + session + Context(time=datetime(1, 1, 1, 0, 5))
    next_state = state.reduce(SolveTask(task_session_id=21))
    updated_session = session._replace(end=datetime(1, 1, 1, 0, 5))
    expected_sessions = EntityMap.from_list([updated_session])
    assert next_state.sessions == expected_sessions


def test_run_program_updating_session():
    session = Session(session_id=1, student_id=1, start=None, end=datetime(1, 1, 1, 0))
    ts = TaskSession(task_session_id=21, student_id=1, task_id=2,
                     start=datetime(1, 1, 1, 0), end=datetime(1, 1, 1, 0))
    state = empty + s1 + t2 + ts + session + Context(time=datetime(1, 1, 1, 0, 5))
    next_state = state.reduce(RunProgram(task_session_id=21, program=None, correct=False))
    updated_session = session._replace(end=datetime(1, 1, 1, 0, 5))
    expected_sessions = EntityMap.from_list([updated_session])
    assert next_state.sessions == expected_sessions


def test_run_program_updating_task_session():
    ts1 = TaskSession(task_session_id=81, student_id=13, task_id=28,
                      start=datetime(1, 1, 1, 10), end=datetime(1, 1, 1, 11))
    ts2 = TaskSession(task_session_id=14, student_id=37, task_id=67,
                      start=datetime(1, 1, 1, 12), end=datetime(1, 1, 1, 12))
    state = empty + ts1 + ts2 + Context(time=datetime(1, 1, 1, 20))
    next_state = state.reduce(RunProgram(task_session_id=14, program=None, correct=False))
    ts2_updated = ts2._replace(end=datetime(1, 1, 1, 20))
    assert next_state.task_sessions == EntityMap.from_list([ts1, ts2_updated])


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


def test_run_program_creates_snapshot():
    ts = TaskSession(task_session_id=14, student_id=37, task_id=67,
                     start=datetime(1, 1, 1, 12), end=datetime(1, 1, 1, 12))
    state = empty + ts + Context(time=datetime(1, 1, 1, 20), new_id=10)
    next_state = state.reduce(RunProgram(task_session_id=14, program='x', correct=False))
    assert next_state.program_snapshots == EntityMap.from_list([
        ProgramSnapshot(program_snapshot_id=10, task_session_id=14, order=1,
                        time=datetime(1, 1, 1, 20), program='x', execution=True, correct=False),
    ])


def test_run_program_creates_snapshot_correct():
    ts = TaskSession(task_session_id=14, student_id=37, task_id=67,
                     start=datetime(1, 1, 1, 12), end=datetime(1, 1, 1, 12))
    state = empty + ts + Context(time=datetime(1, 1, 1, 20), new_id=10)
    next_state = state.reduce(RunProgram(task_session_id=14, program='x', correct=True))
    assert next_state.program_snapshots == EntityMap.from_list([
        ProgramSnapshot(program_snapshot_id=10, task_session_id=14, order=1,
                        time=datetime(1, 1, 1, 20), program='x', execution=True, correct=True),
    ])


def test_run_program_again_creates_another_snapshot():
    ts = TaskSession(
        task_session_id=14,
        student_id=37,
        task_id=67,
        start=datetime(1, 1, 1, 12),
        end=datetime(1, 1, 1, 12))
    ps = ProgramSnapshot(
        program_snapshot_id=10,
        task_session_id=14,
        order=1,
        time=datetime(1, 1, 1, 20),
        program='x',
        execution=False,
        correct=None)
    state = State.build(
        ts, ps,
        Context(time=datetime(1, 1, 1, 20), new_id=10))
    next_state = state.reduce(RunProgram(task_session_id=14, program='y', correct=True))
    assert next_state.program_snapshots == EntityMap.from_list([
        ps,
        ProgramSnapshot(
            program_snapshot_id=10,
            task_session_id=14,
            order=2,
            time=datetime(1, 1, 1, 20),
            program='y',
            execution=True,
            correct=True),
    ])


def test_edit_program_creates_snapshot():
    ts = TaskSession(task_session_id=14, student_id=37, task_id=67,
                     start=datetime(1, 1, 1, 12), end=datetime(1, 1, 1, 12))
    state = empty + ts + Context(time=datetime(1, 1, 1, 20), new_id=10)
    next_state = state.reduce(EditProgram(task_session_id=14, program='x'))
    assert next_state.program_snapshots == EntityMap.from_list([
        ProgramSnapshot(
            program_snapshot_id=10,
            task_session_id=14,
            order=1,
            time=datetime(1, 1, 1, 20),
            program='x',
            execution=False,
            correct=None),
    ])


def test_identity_defaultdict():
    initial_dict = {'a': 1}
    processed_dict = reducers.identity_defaultdict(initial_dict)
    assert processed_dict == initial_dict
    assert processed_dict['b']('S', 'a') == 'S'


def test_identity_reducer():
    state = {'x': [10, 20]}
    assert reducers.identity_reducer(state, 'action') == {'x': [10, 20]}
