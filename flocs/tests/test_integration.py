from flocs.actions import solve_task
from flocs.entities import Student, TaskInstance
from flocs.store import Store

## TODO: revive these tests
#def test_store_integration():
#    def create_my_entities():
#        return {
#            'students': LazyValue(lambda: {
#                0: Student(student_id=0),
#                1: Student(student_id=1),
#            }),
#            'task_instances': LazyValue(lambda: {
#                0: TaskInstance(
#                    task_instance_id=0,
#                    task_id=0,
#                    student_id=0,
#                    solved=False,
#                    given_up=False,
#                ),
#            }),
#        }
#
#    class MyContext(Context):
#        @property
#        def time(self):
#            return datetime(2000, 1, 2)
#
#        @property
#        def randomness_seed(self):
#            return  5
#
#        @property
#        def next_id(self, entity_name):
#            if entity_name == 'task_instances':
#                return 1
#            return 0
#
#    def my_post_commit(self, actions, state, diff):
#        pass  # store actions and apply diff
#
#    def open_my_store():
#        return Store.open(
#            state_creator=create_my_state,
#            context=MyContext(),
#            context_creator=create_my_context,
#            post_commit_hook=my_post_commit)
#
#    with open_my_store() as store:
#        action = solve_task(task_instance_id=0, context=store.context)
#        store.stage_action(action)
#
#    # TODO: using mock test, that my_post_commit was called with
#    # 1) action which includes correct context
#    # 2) LAZY_STATE_2 (with correct context)
#    # 3) correct diff
#    # THEN: similar test for start_task (creating id)
#    assert my_hooks.stored_state == LAZY_STATE_2
