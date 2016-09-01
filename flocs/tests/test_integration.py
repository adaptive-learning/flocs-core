import pytest
from flocs import actions
from flocs.entities import Student, TaskInstance
from flocs.store import Store
from flocs.tests.fixtures_entities import entities_01, entities_02


#@pytest.fixture
#def persistence_hooks():
#    class PersistenceHooks(Store.Hooks):
#        """Fake persistence by storing changes as instance attributes
#        """
#        def __init__(self):
#            self.stored_state = None
#            self.stored_diff = None
#            self.stored_actions = None
#        def post_commit(self, state, diff, actions):
#            self.stored_state = state
#            self.stored_diff = diff
#            self.stored_action = actions
#    return persistence_hooks()
#
#
#def test_integration(persistence_hooks, entities_01, entities_02):
#    with Store.open(entities_01, hooks=persistence_hooks) as store:
#        action = actions.solve_task(task_instance_id=0).at(store.state)
#        store.stage_action(action)
#    assert persistence_hooks.stored_state.entities == entities_02
#
#
##    class MyContext(Context):
##        @property
##        def time(self):
##            return datetime(2000, 1, 2)
##
##        @property
##        def randomness_seed(self):
##            return  5
##
##        @property
##        def next_id(self, entity_name):
##            if entity_name == 'task_instances':
##                return 1
##            return 0
##
##    def my_post_commit(self, actions, state, diff):
##        pass  # store actions and apply diff
##
##    def open_my_store():
##        return Store.open(
##            state_creator=create_my_state,
##            context=MyContext(),
##            context_creator=create_my_context,
##            post_commit_hook=my_post_commit)
##
##    with open_my_store() as store:
##        action = solve_task(task_instance_id=0, context=store.context)
##        store.stage_action(action)
##
##    # TODO: using mock test, that my_post_commit was called with
##    # 1) action which includes correct context
##    # 2) LAZY_STATE_2 (with correct context)
##    # 3) correct diff
##    # THEN: similar test for start_task (creating id)
##    assert my_hooks.stored_state == LAZY_STATE_2
