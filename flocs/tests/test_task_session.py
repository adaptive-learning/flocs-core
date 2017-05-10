from flocs.entities import TaskSession
from flocs.state import empty
from flocs.task_session import get_student_id


def test_get_student_id():
    state = empty + TaskSession(task_session_id=35, student_id=22, task_id=2, start=0, end=0)
    student_id = get_student_id(state, 35)
    assert student_id == 22

# TODO: Add tests for other functions
