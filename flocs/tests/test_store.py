""" Unit and integration tests for flocs.store
"""
from datetime import datetime, timedelta
import pytest
from flocs import actions
from flocs.actions import StartTask
from flocs.context import static, SimulationContext
from flocs.entities import Action, Student, Task, TaskSession, Session
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
    simulation_context = SimulationContext(time=datetime(1, 1, 1, 0, 0, 0))
    store = Store(context=simulation_context)
    assert store.state.context.time == datetime(1, 1, 1, 0, 0, 0)
    store.context.time += timedelta(minutes=20)
    store.add(actions.empty)
    assert store.state.context.time == datetime(1, 1, 1, 0, 20, 0)


def test_current_state():
    state = empty + s1 + t1
    store = Store(state=state, context=static)
    action = StartTask(student_id=1, task_id=1)
    store.add(action)
    expected_state = state.reduce(action)
    assert store.state == expected_state


def test_commmit():
    store = Store(state=empty + s1 + t1, context=static)
    action = StartTask(student_id=1, task_id=1)
    store.add(action)
    store.commit()
    expected_state = (empty + s1 + t1).reduce(action)
    assert store.actions == []
    assert store.state == expected_state


def test_store_integration(mock_hooks):
    """ Test integretion of store, state, context and actions
    """
    with Store.open(state=empty + s1 + t1, context=static, hooks=mock_hooks) as store:
        action = store.add(StartTask(student_id=1, task_id=1))
    expected_state = (empty + s1 + t1).reduce(action)
    expected_diff = [
        (Action, 0, action),
        (TaskSession, 0,
         TaskSession(task_session_id=0, student_id=1, task_id=1,
                     start=static.time, end=static.time)),
        (Session, 0,
         Session(session_id=0, student_id=1, start=static.time, end=static.time)),
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
        action = actions.create(type='start-session', data={})
        store.add(action)
    student = list(store.state.students.values())[0]
    assert student.student_id is not None
    assert student.credits == 0
