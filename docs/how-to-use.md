# How to use

Basic example:

```python
>>> from flocs.actions import StartSession, StartTask
>>> from flocs.store import Store
>>> from flocs.state import default

>>> store = Store(state=default)
>>> a1 = store.add(StartSession())
>>> student_id = a1.data.student_id
>>> a2 = store.add(StartTask(student_id=student_id, task_id='three-steps-forward'))
>>> print(store.state.task_sessions)
TaskSession entities:
* TaskSession(task_session_id=UUID('...'), student_id=UUID('...'), task_id='three-steps-forward', solved=False, ...)
>>> print(store.state.actions.order_by('time'))
Action entities:
* Action(action_id=UUID(...), type='start-session', ...)
* Action(action_id=UUID(...), type='start-task', ...)

```

## Persistence

1. First, specify how to load entities you want to work with.
   Flocs provides `flocs.entity_map.EntityMap`, but you can use your own implementation of entity map,
   e.g. as an adapter over a DB, just make sure to satisfy EntityMap protocol
   (= collections.abc.Mapping protocol, immutable `set`, Django-like `filter` and `order_by`).
   Test your implementation using inheritable `flocs.tests.test_entity_map.TestEntityMap`.

    ```python
    >>> from flocs.entities import Action, Task, Student, TaskSession
    >>> from flocs.state import State
    >>> from flocs.context import dynamic
    >>> from flocs.entity_map import EntityMap

    >>> def my_entity_map(entity_class):
    ...     return EntityMap()  # use your own implementation

    >>> my_entities = {
    ...   entity_class: my_entity_map(entity_class)
    ...   for entity_class in [Action, Task, Student, TaskSession]
    ... }
    >>> my_state = State(entities=my_entities).add_context(dynamic)

    ```

2. Then you need to specify how to store new state.
   You can use `post_commit` hook which is called after each commit in the store.

    ```python
    >>> from flocs.store import Store

    >>> class PersistenceHooks(Store.Hooks):
    ...    def post_commit(self, state, diff):
    ...        pass  # save new state

    ```

3. Finally, use `Store.open()` context manager which creates state at the beginning of the `with` block
   and commits all staged actions at the end of the block.

    ```python
    >>> from flocs import actions
    >>> from flocs.store import Store

    >>> with Store.open(my_state, hooks=PersistenceHooks()) as store:
    ...     action = actions.create(type='nothing-happens', data={})
    ...     store.add(action)
    Action(action_id=UUID(...), type='nothing-happens', ...)

    ```

4. As you are likely to use the same state creator and hooks together many times, you may wish to factor out the creation of store context manager into a separate function:

    ```python
    def open_my_persistent_store():
        return Store.open(my_state, hooks=PersistenceHooks())

    with open_my_persistent_store() as store:
        action = actions.create(type='solve-task', data={'task-session-id': 25})
        store.stage_action(action)
    ```

5. If your persistent state is shared by several threads (e.g. web application), then it is probably good idea to wrap your store operations in an atomic context to avoid inconsistencies.


## Simulation

Flocs can be also used for simulations.
Just use `SimulationContext`, set randomness seed (or use the default one) and change time as needed.

    >>> from flocs.context import SimulationContext
    >>> from flocs.state import default
    >>> from flocs.store import Store
    >>> from flocs.actions import StartSession, StartTask

    >>> context = SimulationContext()
    >>> store = Store(state=default, context=context)

    >>> a1 = store.add(StartSession(student_id=1))
    >>> a2 = store.add(StartTask(student_id=1, task_id='ladder'))
    >>> a1.data.session_id == a2.data.session_id
    True
    >>> a3 = store.add(StartSession(student_id=1))
    >>> # not enough time passed since last action in the current session,
    >>> # so this action intent is ignored and fake action with current
    >>> # session id is returned
    >>> a3.action_id is None
    True
    >>> a1.data == a3.data
    True

    >>> # move time forward
    >>> from datetime import timedelta
    >>> store.context.time += timedelta(hours=10)
    >>> # now it is possible to create new session
    >>> a4 = store.add(StartSession(student_id=1))
    >>> a4.data.session_id != a1.data.session_id
    True
    >>> a4.time
    datetime.datetime(1, 1, 1, 10, 0)

    >>> print(store.state.students)
    Student entities:
    * Student(student_id=1, credits=0)

    >>> print(store.state.sessions.order_by('end'))
    Session entities:
    * Session(..., student_id=1, ..., end=datetime.datetime(1, 1, 1, 0, 0))
    * Session(..., student_id=1, ..., end=datetime.datetime(1, 1, 1, 10, 0))

    >>> print(store.state.task_sessions)
    TaskSession entities:
    * TaskSession(..., student_id=1, task_id='ladder', ...)

    >>> print(store.state.actions.order_by('time'))
    Action entities:
    * Action(..., type='start-session', ...)
    * Action(..., type='start-task', ...)
    * Action(..., type='start-session', ...)


## Tests

Test cases can be created easily using convenient State builder and reducer.

    >>> from datetime import datetime
    >>> from flocs.state import empty
    >>> from flocs.context import Context
    >>> from flocs.entities import Session
    >>> from flocs.actions import StartSession
    >>> from flocs.tests.fixtures_entities import s1, t1, t2

    >>> # create new state with 1 student, 2 tasks and specific time
    >>> state = empty + s1 + t1 + t2 + Context(time=datetime(2017, 1, 1, 12))
    >>> # reduce an action
    >>> next_state = state.reduce(StartSession(student_id=3))
    >>> # assert something about new state
    >>> new_session = Session(session_id=0, student_id=3, start=datetime(2017, 1, 1, 12, 0), end=datetime(2017, 1, 1, 12, 0))
    >>> expected_sessions = (state + new_session).sessions
    >>> assert next_state.sessions == expected_sessions
