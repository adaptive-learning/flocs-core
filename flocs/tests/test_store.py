"""Unit and integration tests of store.py
"""
from itertools import count
import pytest
from flocs import actions
from flocs.context import static_context_generator
from flocs.entities import Student, TaskSession
from flocs.store import Store, compute_entities_diff
from flocs.tests.fixtures_states import STATES


@pytest.fixture
def mock_hooks():
    class MockHooks(Store.Hooks):
        """Fake persistence by storing changes as instance attributes
        """
        # pylint:disable=too-few-public-methods
        def __init__(self):
            self.calls = []
        def post_commit(self, state, diff, actions):
            self.calls.append(('post_commit', state, diff, actions))
    return MockHooks()


def test_store_hooks_called(mock_hooks):
    with Store.open({}, context_generator=static_context_generator, hooks=mock_hooks) as store:
        store.stage_action(actions.EMPTY_ACTION)
    expected_hook_calls = [('post_commit', store.state, [], [actions.EMPTY_ACTION])]
    assert mock_hooks.calls == expected_hook_calls


def test_context_is_changing():
    store = Store({}, context_generator=count)
    assert store.state.context == 1
    assert store.state.context == 2
    store.stage_action(actions.EMPTY_ACTION)
    assert store.state.context == 3


def test_current_state():
    store = Store(STATES['s1'].entities, context_generator=static_context_generator)
    action = actions.solve_task(task_session_id=14).at(store.state)
    store.stage_action(action)
    assert store.state == STATES['s2']


def test_commmit():
    store = Store(STATES['s1'].entities, context_generator=static_context_generator)
    action = actions.solve_task(task_session_id=14).at(store.state)
    store.stage_action(action)
    store.commit()
    assert store.actions == []
    assert store.state == STATES['s2']


def test_integration(mock_hooks):
    with Store.open(STATES['s1'].entities, hooks=mock_hooks) as store:
        action = actions.solve_task(task_session_id=14).at(store.state)
        store.stage_action(action)
    assert len(mock_hooks.calls) == 1
    assert mock_hooks.calls[0][0] == 'post_commit'
    stored_state, stored_diff, stored_actions = mock_hooks.calls[0][1:]
    assert stored_state.entities == STATES['s2'].entities
    assert stored_diff == [(TaskSession, 14, STATES['s2'].entities[TaskSession][14])]
    assert stored_actions == [action]


def test_computes_entities_diff():
    old = {Student: {1: 'a', 2: 'b'}, TaskSession: {1: 'x', 3: 'z'}}
    new = {Student: {1: 'a', 2: 'B'}, TaskSession: {2: 'y', 3: 'z'}}
    diff = compute_entities_diff(old, new)
    assert set(diff) == {(Student, 2, 'B'), (TaskSession, 1, None), (TaskSession, 2, 'y')}
