"""Worldstates for testing purposes
"""
from collections import ChainMap
from flocs.state import State
from flocs.state import STATIC_ENTITIES
from flocs.context import STATIC_CONTEXT
from flocs.entities import TaskSession, Task, Student
from flocs.tests.fixtures_entities import task_sessions_dict, tasks_dict, students_dict


STATES = {
    's0': State.create(
        entities=ChainMap({}, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's1': State.create(
        entities=ChainMap({
            TaskSession: task_sessions_dict('ts1', 'ts2'),
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's2': State.create(
        entities=ChainMap({
            TaskSession: task_sessions_dict('ts1', 'ts2s'),
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's3': State.create(
        entities=ChainMap({
            TaskSession: task_sessions_dict('ts1', 'ts2s'),
            Task: tasks_dict('t1', 't2', 't3'),
            Student: students_dict('stud1', 'stud2', 94)
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's4': State.create(
        entities=ChainMap({
            Student: students_dict('s_new')
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's5': State.create(
        entities=ChainMap({
            TaskSession: task_sessions_dict('ts2s', 'ts3s'),
            Task: tasks_dict('t1', 't2', 't3'),
            Student: students_dict('stud2')
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's6': State.create(
        entities=ChainMap({
            Student: students_dict('stud1')
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
}
