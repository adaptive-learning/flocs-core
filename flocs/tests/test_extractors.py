""" Unit tests for extractors
"""
from datetime import datetime
from flocs.context import Context
from flocs.extractors import get_current_session_id
from flocs.extractors import get_student_id_for_task_session
from flocs.extractors import get_next_snapshot_order
from flocs.state import empty, State
from flocs.entities import TaskSession, Session, ProgramSnapshot


def test_get_current_session_id_single_session():
    session = Session(session_id=17, student_id=21, start=None, end=datetime(1, 1, 1, 0))
    state = empty + session + Context(time=datetime(1, 1, 1, 0))
    session_id = get_current_session_id(state, student_id=21)
    assert session_id == 17


def test_get_current_session_id_latest():
    session1 = Session(session_id=17, student_id=21, start=None, end=datetime(1, 1, 1, 0))
    session2 = Session(session_id=15, student_id=21, start=None, end=datetime(1, 1, 1, 9))
    state = empty + session1 + session2 + Context(time=datetime(1, 1, 1, 9))
    session_id = get_current_session_id(state, student_id=21)
    assert session_id == 15


def test_get_current_session_id_multiple_students():
    session1 = Session(session_id=17, student_id=21, start=None, end=datetime(1, 1, 1, 8, 50))
    session2 = Session(session_id=15, student_id=22, start=None, end=datetime(1, 1, 1, 9))
    state = empty + session1 + session2 + Context(time=datetime(1, 1, 1, 9))
    session_id = get_current_session_id(state, student_id=21)
    assert session_id == 17


def test_get_current_session_first_session():
    session = Session(session_id=15, student_id=22, start=None, end=datetime(1, 1, 1, 9))
    state = empty + session + Context(time=datetime(1, 1, 1, 9), new_id=17)
    session_id = get_current_session_id(state, student_id=21)
    assert session_id == 17


def test_get_current_session_old_session():
    session = Session(session_id=15, student_id=21, start=None, end=datetime(1, 1, 1, 0))
    state = empty + session + Context(time=datetime(1, 1, 3, 0), new_id=17)
    session_id = get_current_session_id(state, student_id=21)
    assert session_id == 17


def test_get_student_id_for_task_session():
    state = empty + TaskSession(task_session_id=35, student_id=22, task_id=2, start=0, end=0)
    student_id = get_student_id_for_task_session(state, 35)
    assert student_id == 22


def test_get_first_snapshot_order():
    state = State.build(
        ProgramSnapshot(program_snapshot_id=10, task_session_id=8, order=1,
                        time=None, program=None, execution=None, correct=None),
        ProgramSnapshot(program_snapshot_id=10, task_session_id=8, order=2,
                        time=None, program=None, execution=None, correct=None),
    )
    next_order = get_next_snapshot_order(state, task_session_id=7)
    assert next_order == 1


def test_get_next_snapshot_order():
    state = State.build(
        ProgramSnapshot(program_snapshot_id=10, task_session_id=7, order=1,
                        time=None, program=None, execution=None, correct=None),
        ProgramSnapshot(program_snapshot_id=11, task_session_id=7, order=2,
                        time=None, program=None, execution=None, correct=None),
        ProgramSnapshot(program_snapshot_id=12, task_session_id=8, order=1,
                        time=None, program=None, execution=None, correct=None),
        ProgramSnapshot(program_snapshot_id=13, task_session_id=8, order=2,
                        time=None, program=None, execution=None, correct=None),
        ProgramSnapshot(program_snapshot_id=14, task_session_id=8, order=3,
                        time=None, program=None, execution=None, correct=None),
        ProgramSnapshot(program_snapshot_id=15, task_session_id=8, order=4,
                        time=None, program=None, execution=None, correct=None),
    )
    next_order = get_next_snapshot_order(state, task_session_id=7)
    assert next_order == 3
