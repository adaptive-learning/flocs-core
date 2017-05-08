""" Unit tests for student
"""
from datetime import datetime, timedelta
from flocs.state import default, empty, State
from flocs.student_extractors import get_student_level, get_active_credits
from flocs.student_extractors import get_student_instructions, StudentInstruction
from flocs.student_extractors import get_student_tasks, StudentTask
from flocs.entities import Student, Instruction, SeenInstruction, TaskSession
from .fixtures_entities import s1, t2, t3


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
        TaskSession(task_session_id=1, student_id=1, task_id=2, solved=False, start=datetime(1, 1, 1, 0, 0, 10),
                    end=datetime(1, 1, 1, 0, 0, 18)),
        TaskSession(task_session_id=2, student_id=1, task_id=2, solved=False, start=datetime(1, 1, 1, 0, 0, 20),
                    end=datetime(1, 1, 1, 0, 0, 25)),
        TaskSession(task_session_id=3, student_id=1, task_id=2, solved=False, start=datetime(1, 1, 1, 0, 0, 30),
                    end=datetime(1, 1, 1, 0, 0, 32)),
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


def test_get_student_level():
    student = Student(student_id=1, credits=20)
    state = default + student
    level = get_student_level(state, student_id=1)
    assert level.level_id == 3


def test_get_active_credits():
    student = Student(student_id=1, credits=20)
    state = default + student
    assert get_active_credits(state, student_id=1) == 7
