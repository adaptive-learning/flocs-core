import pytest
from itertools import count
from flocs import actions
from flocs.context import static_context_generator
from flocs.entities import Student, TaskInstance
from flocs.store import Store, compute_entities_diff
from flocs.tests.fixtures_entities import entities_00, entities_01, entities_02
from flocs.tests.fixtures_states import state_01, state_02


@pytest.fixture
def mock_hooks():
    class MockHooks(Store.Hooks):
        """Fake persistence by storing changes as instance attributes
        """
        def __init__(self):
            self.calls = []
        def post_commit(self, state, diff, actions):
            self.calls.append(('post_commit', state, diff, actions))
    return MockHooks()


def test_store_hooks_called(mock_hooks, entities_00):
    with Store.open(entities_00, context_generator=static_context_generator, hooks=mock_hooks) as store:
        store.stage_action(actions.EMPTY_ACTION)
    expected_hook_calls = [('post_commit', store.state, [], [actions.EMPTY_ACTION])]
    assert mock_hooks.calls == expected_hook_calls


def test_context_is_changing(entities_00):
    store = Store(entities_00, context_generator=count)
    assert store.state.context == 1
    assert store.state.context == 2
    store.stage_action(actions.EMPTY_ACTION)
    assert store.state.context == 3


def test_current_state(state_01, state_02):
    store = Store(state_01.entities, context_generator=static_context_generator)
    action = actions.solve_task(task_instance_id=14).at(store.state)
    store.stage_action(action)
    assert store.state == state_02


def test_commmit(state_01, state_02):
    store = Store(state_01.entities, context_generator=static_context_generator)
    action = actions.solve_task(task_instance_id=14).at(store.state)
    store.stage_action(action)
    store.commit()
    assert store.actions == []
    assert store.state == state_02


def test_integration(mock_hooks, entities_01, entities_02):
    with Store.open(entities_01, hooks=mock_hooks) as store:
        action = actions.solve_task(task_instance_id=14).at(store.state)
        store.stage_action(action)
    assert len(mock_hooks.calls) == 1
    assert mock_hooks.calls[0][0] == 'post_commit'
    stored_state, stored_diff, stored_actions = mock_hooks.calls[0][1:]
    assert stored_state.entities == entities_02
    assert stored_diff == [(TaskInstance, 14, entities_02[TaskInstance][14])]
    assert stored_actions == [action]


def test_computes_entities_diff():
    old = {Student: {1: 'a', 2: 'b'}, TaskInstance: {1: 'x', 3: 'z'}}
    new = {Student: {1: 'a', 2: 'B'}, TaskInstance: {2: 'y', 3: 'z'}}
    diff = compute_entities_diff(old, new)
    assert set(diff) == {(Student, 2, 'B'), (TaskInstance, 1, None), (TaskInstance, 2, 'y')}
