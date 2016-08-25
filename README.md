# flocs-core


## Usage

1. Implement state creator to specify how to load the state:


```python
from flocs.state import State, LazyValue

def create_my_state():
    state = State({
      'entities.students': LazyValue(get_all_students),
      'entities.task_instances': LazyValue(get_all_task_instances),
      'context.time': datetime.now(),
      'context.randomness_seed': random.randint(0, sys.maxsize),
    })
    return state
```

2. Implement `post_commit` hook to specify how to store the state:


```python
from flocs.store import Store

class PersistenceHooks(Store.Hooks):
    def post_commit(self, state, diff):
        pass  # save new state

my_persistence_hooks = PersistenceHooks()
```

3. Then you can use `Store.open()` context manager which creates state at the beginning of the `with` block and commits all staged actions at the end of the block.

```python
from flocs.actions import ActionCreators

with Store.open(create_my_state, hooks=my_persistence_hooks) as store:
    action = ActionCreators.solve_task(task_instance_id=0)
    store.stage_action(action)
```

### Tips

As you are likely to use the same state creater and hooks together many times, you may wish to factor out the creation of store context manager into a separate function:

```python
def open_my_persistent_store():
    return Store.open(create_my_state, hooks=my_persistence_hooks)

with open_my_persistent_store() as store:
    action = ActionCreators.solve_task(task_instance_id=0)
    store.stage_action(action)
```

