# Flow of Computer Science

Flocs is a Python and a NPM package of components for adaptive learning of computer science aiming at creating a [flow experience][1].
It provides models, techniques, simulations and visualizations.
Flocs is developed by [Adaptive Learning group][2] at Faculty of informatics, Masaryk university.

  [1]: https://en.wikipedia.org/wiki/Flow_(psychology)
  [2]: http://www.fi.muni.cz/adaptivelearning/

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

Python flocs package can be installed with:

```
pip install flocs
```

Essential links:

* [Concepts Overview](https://github.com/adaptive-learning/flocs-core/blob/master/docs/concepts-overview.md)
* [How to Use](https://github.com/adaptive-learning/flocs-core/blob/master/docs/how-to-use.md)
* [How to Develop](https://github.com/adaptive-learning/flocs-core/blob/master/docs/how-to-develop.md)
* [Issue Tracker](https://github.com/adaptive-learning/flocs-core/issues)
