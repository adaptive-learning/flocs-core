""" Unit tests for extractors
"""
from datetime import datetime, timedelta
from flocs.extractors import get_level, get_active_credits, get_recommendation
from flocs.extractors import get_student_instructions, StudentInstruction
from flocs.extractors import get_student_tasks, StudentTask
from flocs.extractors import get_practice_overview, PracticeOverview
from flocs.state import default, empty, State
from flocs.entities import Student, Instruction, SeenInstruction, TaskSession
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
        + TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, time_start=30, time_end=40)
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=True, time=10),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_with_unsolved_task_session():
    state = empty + s1 + t2 + t3 \
        + TaskSession(task_session_id=1, student_id=1, task_id=2, time_start=30, time_end=40)
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=False, time=10),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_best_solved_time():
    state = State.build(
        s1, t2, t3,
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, time_start=10, time_end=18),
        TaskSession(task_session_id=2, student_id=1, task_id=2, solved=True, time_start=20, time_end=25),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=True, time_start=30, time_end=39),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=False, time_start=40, time_end=41),
    )
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=True, time=5),
        StudentTask(task_id=3, solved=False, time=None),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_best_solved_datetime():
    state = State.build(
        s1, t2,
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True,
            time_start=datetime(2017, 1, 10, 5, 30, 10),
            time_end=datetime(2017, 1, 10, 5, 30, 17)),
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True,
            time_start=datetime(2017, 1, 10, 5, 30, 20),
            time_end=datetime(2017, 1, 10, 5, 30, 23))
    )
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=True, time=timedelta(seconds=3)),
    }
    assert set(student_tasks) == expected_student_tasks


def test_get_student_tasks_last_unsolved_time():
    state = State.build(
        s1, t2, t3,
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=False, time_start=10, time_end=18),
        TaskSession(task_session_id=2, student_id=1, task_id=2, solved=False, time_start=20, time_end=25),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=False, time_start=30, time_end=32),
    )
    student_tasks = get_student_tasks(state, student_id=1)
    expected_student_tasks = {
        StudentTask(task_id=2, solved=False, time=2),
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
    student = Student(student_id=1, last_task_session_id=None, credits=20)
    state = default + student
    level = get_level(state, student_id=1)
    assert level.level_id == 3


def test_get_active_credits():
    student = Student(student_id=1, last_task_session_id=None, credits=20)
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
    state = State.build(s1, t2, TaskSession(student_id=1, task_id=2, solved=True, time_start=30, time_end=40))
    overview = get_practice_overview(state, student_id=1)
    assert overview.tasks == [StudentTask(task_id=2, solved=True, time=10)]
