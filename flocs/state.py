"""
Representation of a world state
"""
from collections import namedtuple
from datetime import datetime
from flocs import __version__
from .data import create_tasks_dict
from .entities import Student, Task, TaskInstance


State = namedtuple('State', [
    'entities',
    'context',
    'meta',
])

#Entities = namedtuple('Entitities', [
#    'students',
#    'tasks',
#    'task_instances',
#    'task_stats',
#])
#
#Context = namedtuple('Context', [
#    'time',
#    'randomness',
#])
#
#Meta = namedtuple('Meta', [
#    'version',
#])


#def create_state(create_entities=create_static_entities, create_context=create_static_context):
#    state = State(
#        meta=create_meta(),
#        context=create_context(),
#        entities=create_entities(),
#    )
#    return state


def create_state(entities, context):
    state = State(
        entities=entities,
        context=context,
        meta=create_meta(),
    )
    return state


def create_static_entities():
    return STATIC_ENTITIES

STATIC_ENTITIES = {
    Student: {},
    Task: create_tasks_dict(),
    TaskInstance: {},
}

def create_static_context():
    return STATIC_CONTEXT

STATIC_CONTEXT = {
    'time': datetime(1, 1, 1),
    'randomness':0,
}


def create_meta():
    return META

META = {
    'version': __version__,
}

#def create_static_entities():
#    entities = Entities(
#        students={},
#        tasks=create_tasks_dict(),
#        task_instances={},
#    )
#    return entities
#
#
#def create_static_context():
#    context = Context(
#        time=datetime(1, 1, 1),
#        randomness_seed=0,
#    )
#
#
#def create_meta():
#    meta = Meta(
#        version=__version__,
#    )
