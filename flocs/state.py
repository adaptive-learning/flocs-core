"""Representation of a world state
"""
from collections import namedtuple
from .data import create_tasks_dict
from .entities import Student, Task, TaskInstance
from .meta import META


class State(namedtuple('State', ['entities', 'context', 'meta'])):
    """Represents state of the world at a specific moment

    Attributes:
        entities - nested mapping: entity type -> id -> entity
        context - mapping for values changing continuously
        meta - mapping for information how to interpret the state
    """
    __slots__ = ()

    @staticmethod
    def create(entities, context=None):
        return State(entities=entities, context=context, meta=META)


STATIC_ENTITIES = {
    Student: {},
    Task: create_tasks_dict(),
    TaskInstance: {},
}
