"""Representation of a world state
"""
from collections import namedtuple
from .data.tasks import TASKS
from .entities import Student, Task, TaskSession
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


def create_static_entities():
    return {
        Student: {},
        Task: create_tasks_dict(),
        TaskSession: {},
    }


def create_tasks_dict():
    return {task.task_id: task for task in TASKS}


STATIC_ENTITIES = create_static_entities()
