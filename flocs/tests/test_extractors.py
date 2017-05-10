""" Unit tests for extractors
"""
from datetime import datetime, timedelta
from flocs.state import default, empty, State
from flocs.extractors import get_practice_overview, get_recommendation, PracticeOverview, Recommendation
from flocs.student import StudentInstruction, StudentTask
from flocs.entities import Instruction, TaskSession
from .fixtures_entities import s1, t2

DEFAULT_RECOMMENDATION_FUNCTION = 'flocs.extractors.random_by_level'
DEFAULT_RECOMMENDED_TASK_ID = 'one-step-forward'


def test_get_recommendation(mocker):
    """ Only checks if the correct recommendation function is internally called.
    """
    random_by_level = mocker.patch(DEFAULT_RECOMMENDATION_FUNCTION)
    random_by_level.return_value = DEFAULT_RECOMMENDED_TASK_ID

    state = default + s1
    recommendation = get_recommendation(state, student_id=1)
    assert recommendation.available
    assert recommendation.task_id == DEFAULT_RECOMMENDED_TASK_ID
    random_by_level.assert_called_once_with(state, 1)


def test_get_practice_overview_empty(mocker):
    random_by_level = mocker.patch(DEFAULT_RECOMMENDATION_FUNCTION)
    random_by_level.return_value = DEFAULT_RECOMMENDED_TASK_ID

    state = empty + s1
    overview = get_practice_overview(state, student_id=1)
    # there are no levels, instructions nor tasks in empty state
    expected_overview = PracticeOverview(
        level=0,
        credits=0,
        active_credits=0,
        instructions=[],
        tasks=[],
        recommendation=Recommendation(available=True, task_id=DEFAULT_RECOMMENDED_TASK_ID)
    )
    assert overview == expected_overview


def test_get_practice_overview_level_and_credits(mocker):
    mocker.patch(DEFAULT_RECOMMENDATION_FUNCTION)

    state = default + s1._replace(credits=8)
    overview = get_practice_overview(state, student_id=1)
    assert overview.level == 2
    assert overview.credits == 8
    assert overview.active_credits == 2


def test_get_practice_overview_with_instructions(mocker):
    mocker.patch(DEFAULT_RECOMMENDATION_FUNCTION)

    state = State.build(s1, Instruction(instruction_id='A'))
    overview = get_practice_overview(state, student_id=1)
    assert overview.instructions == [StudentInstruction(instruction_id='A', seen=False)]


def test_get_practice_overview_with_tasks(mocker):
    mocker.patch(DEFAULT_RECOMMENDATION_FUNCTION)

    ts = TaskSession(student_id=1, task_id=2, solved=True,
                     start=datetime(1, 1, 1, 0, 0, 30), end=datetime(1, 1, 1, 0, 0, 40))
    state = State.build(s1, t2, ts)
    overview = get_practice_overview(state, student_id=1)
    assert overview.tasks == [StudentTask(task_id=2, solved=True, time=timedelta(seconds=10))]
