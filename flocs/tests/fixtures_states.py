"""Worldstates for testing purposes
"""
from collections import ChainMap
from flocs.state import State
from flocs.state import STATIC_ENTITIES
from flocs.context import STATIC_CONTEXT
from flocs.entities import TaskInstance
from flocs.tests.fixtures_entities import task_instances_dict


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
}
