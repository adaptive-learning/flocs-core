"""Worldstates for testing purposes
"""
from collections import ChainMap
from flocs.state import State
from flocs.state import STATIC_ENTITIES
from flocs.context import STATIC_CONTEXT
from flocs.entities import TaskInstance, Task, Student
from flocs.tests.fixtures_entities import task_instances_dict, tasks_dict, students_dict


STATES = {
    's0': State.create(
        entities=ChainMap({}, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's1': State.create(
        entities=ChainMap({
            TaskInstance: task_instances_dict('ti1', 'ti2'),
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's2': State.create(
        entities=ChainMap({
            TaskInstance: task_instances_dict('ti1', 'ti2s'),
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
    's3': State.create(
        entities=ChainMap({
            TaskInstance: task_instances_dict('ti1', 'ti2s'),
            Task: tasks_dict('t1', 't2'),
            Student: students_dict('stud1', 'stud2')
        }, STATIC_ENTITIES),
        context=STATIC_CONTEXT,
    ),
}
