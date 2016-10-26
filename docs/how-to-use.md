# How to use

Basic example:

```python
from flocs.actions import create_student, solve_task
from flocs.state import STATIC_ENTITIES
from flocs.store import Store

# create a store by specifying initial entities and optionally a context generator
store = Store(STATIC_ENTITIES)

# create an action and set its context by `at` operator
action = create_student(student_id=1).at(store.state)

# stage action to store
store.stage_action(action)

# create and stage another actions
action = actions.solve_task(student_id=1, task_id=1).at(store.state)
store.stage_action(action)

# current state is computed on demand by applying all staged actions to initial state
# (and also generating current context)
print(store.state.entities)
```

## Persistence

1. First, specify how to load entities you want to work with.
   Entities must provide nested mapping `entity type -> id -> entity`.
   However, it does not need to be a dict, so you can e.g. implement lazy loading from DB.

    ```python
    from collections import ChainMap
    from flocs.entities import Student, TaskSession
    from flocs.state import STATIC_ENTITIES

    dynamic_entities = {
        Student: load_students(),
        TaskSession: load_task_sessions(),
    }
    my_entities = ChainMap(new_entities, STATIC_ENTITIES)
    ```

2. Then you need to specify how to store new state (and performed actions).
   One way is to to implement `post_commit` hook which will be called after commit in the store.

    ```python
    from flocs.store import Store

    class PersistenceHooks(Store.Hooks):
        def post_commit(self, state, diff, actions):
            pass  # save new state and actions
    ```

3. Finally, use `Store.open()` context manager which creates state at the beginning of the `with` block
   and commits all staged actions at the end of the block.

    ```python
    from flocs import actions
    from flocs.store import Store

    with Store.open(my_entities, hooks=PersistenceHooks()) as store:
        action = actions.solve_task(task_session_id=14).at(store.state)
        store.stage_action(action)
    ```

### Tips

* As you are likely to use the same state creator and hooks together many times, you may wish to factor out the creation of store context manager into a separate function:

    ```python
    def open_my_persistent_store():
        return Store.open(my_entities, hooks=PersistenceHooks())

    with open_my_persistent_store() as store:
        action = actions.solve_task(task_session_id=14).at(store.state)
        store.stage_action(action)
    ```

* If your persistent state is shared by several threads (e.g. web application), then it is probably good idea to wrap your store operations in an atomic context to avoid inconsistencies.
