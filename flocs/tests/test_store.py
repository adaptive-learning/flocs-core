""" Unit and integration tests for flocs.store
"""
from datetime import datetime, timedelta
import pytest
from flocs import actions
from flocs.context import static, SimulationContext
from flocs.entities import Action, Student, Task, TaskSession
from flocs.state import empty
from flocs.store import Store, compute_entities_diff
from .fixtures_entities import s1, t1, t2, t3


@pytest.fixture
def mock_hooks():
    class MockHooks(Store.Hooks):
        """Fake persistence by storing changes as instance attributes
        """
        # pylint:disable=too-few-public-methods
        def __init__(self):
            self.calls = []
        def post_commit(self, state, diff):
            self.calls.append(('post_commit', state, diff))
    return MockHooks()


def test_store_hooks_called(mock_hooks):
    with Store.open(state=empty, context=static, hooks=mock_hooks):
        pass
    expected_hook_calls = [('post_commit', empty + static, [])]
    assert mock_hooks.calls == expected_hook_calls


def test_context_is_changing():
    initial_time = datetime(1, 1, 1, 0, 0, 0)
    time_step = timedelta(minutes=1)
    simulation_context = SimulationContext(initial_time=initial_time, time_step=time_step)
    store = Store(context=simulation_context)
    time1 = store.state.time
    store.stage_action(actions.empty)
    time2 = store.state.time
    assert time1 == initial_time
    assert time2 == initial_time + time_step


def test_current_state():
    store = Store(state=empty + s1 + t1, context=static)
    action = actions.create(type='start-task', data={'student-id': 1, 'task-id': 1})
    store.stage_action(action)
    expected_state = empty + static + s1 + t1 + action.add_context(static)
    assert store.state == expected_state


def test_commmit():
    store = Store(state=empty + s1 + t1, context=static)
    action = actions.create(type='start-task', data={'student-id': 1, 'task-id': 1})
    store.stage_action(action)
    store.commit()
    expected_state = empty + static + s1 + t1 + action.add_context(static)
    assert store.actions == []
    assert store.state == expected_state


def test_store_integration(mock_hooks):
    """ Test integretion of store, state, context and actions
    """
    with Store.open(state=empty + s1 + t1, context=static, hooks=mock_hooks) as store:
        action = actions.create(
            type='start-task',
            data={'student-id': 1, 'task-id': 1},
            context=static)
        store.stage_action(action)
    expected_state = empty + static + s1 + t1 + action.add_context(static)
    expected_diff = [
        (Action, 0,
         action.add_context(static)),
        (Student, 1,
         Student(student_id=1, last_task_session_id=0, credits=0)),
        (TaskSession, 0,
         TaskSession(task_session_id=0, student_id=1, task_id=1, time_start=static.time, time_end=static.time)),
    ]
    assert len(mock_hooks.calls) == 1
    assert mock_hooks.calls[0][0] == 'post_commit'
    stored_state, stored_diff = mock_hooks.calls[0][1:]
    assert stored_state == expected_state
    assert set(stored_diff) == set(expected_diff)


def test_compute_entities_diff():
    old = empty + s1 + t1
    s1_b = s1._replace(credits=100)
    new = empty + s1_b + t1 + t2 + t3
    diff = compute_entities_diff(old.entities, new.entities)
    assert set(diff) == {(Student, 1, s1_b), (Task, 2, t2), (Task, 3, t3)}


def test_reducing_action_without_optional_parameters():
    """Covers issue #52
    See https://github.com/adaptive-learning/flocs-core/issues/52
    """
    with Store.open(state=empty) as store:
        action = actions.create(type='create-student', data={}, context=static)
        store.stage_action(action)
    student = list(store.state.entities[Student].values())[0]
    assert student.last_task_session_id is None
