# Flow of Computer Science

Flocs is a Python and a NPM package of components for adaptive learning of computer science aiming at creating a [flow experience][1].
It provides models, techniques, simulations and visualizations.
Flocs is developed by [Adaptive Learning group][2] at Faculty of informatics, Masaryk university.

  [1]: https://en.wikipedia.org/wiki/Flow_(psychology)
  [2]: http://www.fi.muni.cz/adaptivelearning/

```python
>>> from flocs.actions import create_student
>>> from flocs.entities import Student
>>> from flocs.state import STATIC_ENTITIES
>>> from flocs.store import Store

>>> store = Store(STATIC_ENTITIES)
>>> action = create_student(student_id=1)
>>> store.stage_action(action)
>>> print(dict(store.state.entities[Student]))
{1: Student(student_id=1, last_task_session_id=None)}
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
