""" Unit tests for extractors
"""
from datetime import datetime, timedelta
from flocs.context import Context
from flocs.extractors import get_level, get_active_credits, get_recommendation
from flocs.extractors import get_student_instructions, StudentInstruction
from flocs.extractors import get_student_tasks, StudentTask
from flocs.extractors import get_practice_overview, PracticeOverview, Recommendation
from flocs.extractors import get_current_session_id
from flocs.extractors import get_student_id_for_task_session
from flocs.extractors import get_next_snapshot_order
from flocs.state import default, empty, State
from flocs.entities import Student, Instruction, SeenInstruction, TaskSession, Session, ProgramSnapshot
from .fixtures_entities import s1, t2, t3


def test_get_recommendation():
    state = default + s1
    recommendation = get_recommendation(state, student_id=1)
    assert recommendation.available
    assert recommendation.task_id == 'one-step-forward'


def test_get_student_tasks_no_task_sessions():
    state = empty + s1 + t2 + t3
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=False, time=None),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_with_solved_task_session():
    state = empty + s1 + t2 + t3 \
        + TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True,
                      start=datetime(1, 1, 1, 0, 0, 30), end=datetime(1, 1, 1, 0, 0, 40))
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=True, time=timedelta(seconds=10)),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_with_unsolved_task_session():
    state = empty + s1 + t2 + t3 \
        + TaskSession(task_session_id=1, student_id=1, task_id=2,
                      start=datetime(1, 1, 1, 0, 0, 30), end=datetime(1, 1, 1, 0, 0, 40))
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=False, time=timedelta(seconds=10)),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_best_solved_time():
    state = State.build(
        s1, t2, t3,
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True,
            start=datetime(1, 1, 1, 0, 0, 10), end=datetime(1, 1, 1, 0, 0, 18)),
        TaskSession(task_session_id=2, student_id=1, task_id=2, solved=True,
            start=datetime(1, 1, 1, 0, 0, 20), end=datetime(1, 1, 1, 0, 0, 25)),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=True,
            start=datetime(1, 1, 1, 0, 0, 30), end=datetime(1, 1, 1, 0, 0, 39)),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=False,
            start=datetime(1, 1, 1, 0, 0, 40), end=datetime(1, 1, 1, 0, 0, 41)),
    )
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=True, time=timedelta(seconds=5)),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_best_solved_datetime():
    state = State.build(
        s1, t2,
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True,
            start=datetime(2017, 1, 10, 5, 30, 10),
            end=datetime(2017, 1, 10, 5, 30, 17)),
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True,
            start=datetime(2017, 1, 10, 5, 30, 20),
            end=datetime(2017, 1, 10, 5, 30, 23))
    )
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=True, time=timedelta(seconds=3)),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_last_unsolved_time():
    state = State.build(
        s1, t2, t3,
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=False, start=datetime(1, 1, 1, 0, 0, 10), end=datetime(1, 1, 1, 0, 0, 18)),
        TaskSession(task_session_id=2, student_id=1, task_id=2, solved=False, start=datetime(1, 1, 1, 0, 0, 20), end=datetime(1, 1, 1, 0, 0, 25)),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=False, start=datetime(1, 1, 1, 0, 0, 30), end=datetime(1, 1, 1, 0, 0, 32)),
    )
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=False, time=timedelta(seconds=2)),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_instructions():
    iA = Instruction(instruction_id='A')
    iB = Instruction(instruction_id='B')
    state = empty + s1 + iA + iB
    state += SeenInstruction(seen_instruction_id=2, student_id=1, instruction_id='B')
    student_instructions = get_student_instructions(state, student_id=1)
    expected_student_instructions = {
        StudentInstruction(instruction_id='A', seen=False),
        StudentInstruction(instruction_id='B', seen=True),
    }
    assert set(student_instructions) == expected_student_instructions


def test_get_student_instructions_all_unseen():
    iA = Instruction(instruction_id='A')
    iB = Instruction(instruction_id='B')
    state = empty + s1 + iA + iB
    student_instructions = get_student_instructions(state, student_id=1)
    expected_student_instructions = {
        StudentInstruction(instruction_id='A', seen=False),
        StudentInstruction(instruction_id='B', seen=False),
    }
    assert set(student_instructions) == expected_student_instructions


def test_get_student_instructions_all_seen():
    iA = Instruction(instruction_id='A')
    iB = Instruction(instruction_id='B')
    state = empty + s1 + iA + iB
    state += SeenInstruction(seen_instruction_id=1, student_id=1, instruction_id='A')
    state += SeenInstruction(seen_instruction_id=2, student_id=1, instruction_id='B')
    student_instructions = get_student_instructions(state, student_id=1)
    expected_student_instructions = {
        StudentInstruction(instruction_id='A', seen=True),
        StudentInstruction(instruction_id='B', seen=True),
    }
    assert set(student_instructions) == expected_student_instructions


def test_get_level():
    student = Student(student_id=1, credits=20)
    state = default + student
    level = get_level(state, student_id=1)
    assert level.level_id == 3


def test_get_active_credits():
    student = Student(student_id=1, credits=20)
    state = default + student
    assert get_active_credits(state, student_id=1) == 7


def test_get_practice_overview_empty():
    state = empty + s1
    overview = get_practice_overview(state, student_id=1)
    expected_overview = PracticeOverview(
        level=0,
        credits=0,
        active_credits=0,
        instructions=[],
        tasks=[],
        recommendation=Recommendation(available=True, task_id='one-step-forward')
    )
    assert overview == expected_overview


def test_get_practice_overview_level_and_credits():
    state = default + s1._replace(credits=10)
    overview = get_practice_overview(state, student_id=1)
    assert overview.level == 2
    assert overview.credits == 10
    assert overview.active_credits == 6


def test_get_practice_overview_with_instructions():
    state = State.build(s1, Instruction(instruction_id='A'))
    overview = get_practice_overview(state, student_id=1)
    assert overview.instructions == [StudentInstruction(instruction_id='A', seen=False)]


def test_get_practice_overview_with_tasks():
    ts = TaskSession(student_id=1, task_id=2, solved=True,
                     start=datetime(1, 1, 1, 0, 0, 30), end=datetime(1, 1, 1, 0, 0, 40))
    state = State.build(s1, t2, ts)
    overview = get_practice_overview(state, student_id=1)
    assert overview.tasks == [StudentTask(task_id=2, solved=True, time=timedelta(seconds=10))]


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
