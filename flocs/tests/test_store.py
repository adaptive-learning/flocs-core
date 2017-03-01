"""Unit and integration tests of store.py
"""
from itertools import count
import pytest
from flocs import actions
from flocs.context import static_context_generator
from flocs.entities import Student, TaskSession
from flocs.state import EntityMap
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


def test_compute_entities_diff():
    old = {
        Student: EntityMap({1: 'a', 2: 'b'}),
        TaskSession: EntityMap({1: 'x', 3: 'y'})
    }
    new = {
        Student: EntityMap({3: 'c'}, old[Student]),
        TaskSession: EntityMap({1: 'z'}, old[TaskSession])
    }
    diff = compute_entities_diff(old, new)
    print('diff', diff)
    assert set(diff) == {(Student, 3, 'c'), (TaskSession, 1, 'z')}


def test_compute_diff():
    old_state = STATES['s1']
    new_state = STATES['s2']
    diff = compute_entities_diff(old_state.entities, new_state.entities)
    assert set(diff) == {(TaskSession, 14, TaskSession(
                          task_session_id=14,
                          student_id=37,
                          task_id=67,
                          solved=True,
                          given_up=False,
                          ))}



def test_reducing_action_without_optional_parameters():
    """Covers issue #52
    See https://github.com/adaptive-learning/flocs-core/issues/52
    """
    with Store.open({Student: EntityMap()}) as store:
        store.stage_action(actions.create_student())
    student = list(store.state.entities[Student].values())[0]
    assert student.last_task_session_id is None
