from flocs.action_creators import solve_task
from flocs.store import Store
from flocs.tests.states import STATE_3, STATE_4


def test_store_context_manager():
    # TODO: use mock and also check that post_commit was called exectly once
    class MyHooks(Store.Hooks):
        def __init__(self):
            self.stored_state = None
        def post_commit(self, state, diff):
            self.stored_state = state
    my_hooks = MyHooks()

    with Store.open(lambda: STATE_3, hooks=my_hooks) as store:
        action = solve_task(task_instance_id=0)
        store.stage_action(action)

    assert my_hooks.stored_state == STATE_4
