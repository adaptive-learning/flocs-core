# Flow of Computer Science

Components for adaptive learning of computer science.
Models, techniques, simulations and visualizations.

## Overview
Architecture, principles, requirements.

Concept | Meaning
------- | ----------
state | snapshot of the world we model in a single moment
state shape | which part of the state describes what
actions | describe events and interaction in the world
reducers | describe how the state changes under the actions
extractors | describe how to extract information from the state

Clients can specify which parts of the state they want to use (state shape).
They can provide a persistence shell, i.e. specify lazy loading of the state and how to store changes in the state.
They should also provide a persistent model for actions.

State, reducers and extractors depend on an agreed state shape, for example an extractor for task selection requires a tasks entities to be present in the state.
Each part of the state is associated with a reducer, that describe how this part of the state changes under all possible actions.
Actions and reducers are orthogonal concepts – one action may cause changes in several parts of the state
(e.g. creating a new attempt will not only change the set of attempts entities, but also update parameters of various skill and difficulty models).

Actions are domain-specific events and interactions, e.g. `start_task`, `solve_task` and `give_up_task`.
Clients does not need to know about the logic behind actions, they even does not need to which parts of the state are changed under which action.
When an action happens, they just delegate the change to the core, passing a current state and action to the reducer, which computes a new state.

An initial state and series of actions are the complete "source of truth"
(code of the reducer is also important, but it is specified by the meta information in each action).
This architecture enables to see how the parameters were changing, as well as well as how they would be changing for different models or parameters, without any additional logs.
It also enables to reconstruct any past state, which can be useful not only if something goes terribly wrong, but also for much easier debugging – one can see how the state changed when a problem occurred, which is great for understanding the situation.

Current state in DB (or in CSV tables) can be viewed as just a derivative of the primary source of truth (initial state and action stream).
This allows to optimize the current state for special purposes of the specific client, e.g. web does not need to have a quick access to the history of the parameters, only the current ones.

There are several extremely important non-functional requirements we follow:
the code should be easy and pleasure to use, to read, to extend and to test.
The code together with the tests should form a beautiful, clear and coherent story.

## Usage


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


### Persistence

1. First, specify how to load entities you want to work with.
   Entities must provide nested mapping `entity type -> id -> entity`.
   However, it does not need to be a dict, so you can e.g. implement lazy loading from DB.

    ```python
    from collections import ChainMap
    from flocs.entities import Student, TaskInstance
    from flocs.state import STATIC_ENTITIES

    dynamic_entities = {
        Student: load_students(),
        TaskInstance: load_task_instances(),
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
        action = actions.solve_task(task_instance_id=14).at(store.state)
        store.stage_action(action)
    ```

### Tips

* As you are likely to use the same state creator and hooks together many times, you may wish to factor out the creation of store context manager into a separate function:

    ```python
    def open_my_persistent_store():
        return Store.open(my_entities, hooks=PersistenceHooks())

    with open_my_persistent_store() as store:
        action = actions.solve_task(task_instance_id=14).at(store.state)
        store.stage_action(action)
    ```

* If your persistent state is shared by several threads (e.g. web application), then it is probably good idea to wrap your store operations in an atomic context to avoid inconsistencies.

