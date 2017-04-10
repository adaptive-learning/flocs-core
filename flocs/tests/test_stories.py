""" Integration tests of complete stories (scenarios)
"""
from datetime import timedelta
from flocs.context import SimulationContext
from flocs.state import empty
from flocs.store import Store
from flocs.actions import StartSession, StartTask
from .fixtures_entities import t1


def test_new_student_session():
    context = SimulationContext()
    state = empty + t1
    store = Store(state=state, context=context)
    a1 = store.add(StartSession())
    a2 = store.add(StartTask(student_id=a1.data.student_id, task_id=1))
    assert a2.data.session_id == a1.data.session_id
    a3 = store.add(StartSession(student_id=a1.data.student_id))
    assert not a3  # discarded
    store.context.time += timedelta(hours=10)  # TODO: should work without store prefix
    a4 = store.add(StartSession(student_id=a1.data.student_id))
    assert a4  is not None  # not discarded
    assert a4.data.session_id != a2.data.session_id
    ## TODO: the following also requries to iterate over items, not keys...
    #assert list(state.students) == [Student(student_id=a1.student_id)]
    ## TODO: the following also requries default by-date ordering
    #assert list(state.sessions) == [
    #    Session(session_id=a1.session_id, student_id=a1.student_id),
    #    Session(session_id=a4.session_id, student_id=a1.student_id)
    #]
    #assert list(state.task_sessions) == [
    #    TaskSession(task_session_id=a2.task_session_id, student_id=a1.student_id, task_id=1)
    #]
    #assert list(state.actions) == [a1, a2, a4]


"""
Use cases:

1) web + actions factory
store = Store(state=db_state, context=dynamic)
action = actions.create(type, **data)  # create action intent
store.add(action)  # fill missing data and context (snapshot from store.context)
store.commit()  # reduce action

2) web + specific action
store = Store(state=db_state, context=dynamic)
store.add(StartSession(student_id=3))

3) simulation
store = Store(state=default, context=SimulationContext(...))
store.add(StartSession(student_id=3))
store.context.time += timedelta(minutes=3)
store.add(StartSession(student_id=3))

4) tests for specific an action-entity pair
state = empty + static + s1 + t1
next_state = state.reduce(StartSession(student_id=3))
assert next_state.sessions == EntityMap.from_list([Session(...)])
"""
