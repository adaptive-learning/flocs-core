"""Representation of a world state
"""
import operator
from collections import namedtuple
from collections import UserDict
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


class EntityMapping(UserDict):
    """Collection of all entities of given type (i.e., 1 entity table)

    Provided interface:
    1. __init__(data) and from_list(entity_list)
    2. collections.abc.Mapping
    3. filter method as in Django QuerySets
    """
    @classmethod
    def from_list(cls, entity_list):
        return cls({get_id(entity): entity for entity in entity_list})

    def filter(self, **kwargs):
        print('filtering', self.data, 'with', kwargs)
        filtered_mapping = EntityMapping({
            i: entity
            for i, entity in self.data.items()
            if self._test_entity(entity, **kwargs)
        })
        return filtered_mapping

    def _test_entity(self, entity, **kwargs):
        """Return True if a given entity satisfies condition by **kwargs

        For full kwargs specification, see Django QuerySet's filter:
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups
        But only a subset of lookups is currently implemented, see single_test
        """
        is_true = all(
            self._test_entity_single(entity, query, right)
            for query, right in kwargs.items())
        return is_true

    def _test_entity_single(self, entity, query, right):
        query_parts = query.split('__')
        left = getattr(entity, query_parts[0])
        query_type = query_parts[1] if len(query_parts) > 1 else 'exact'
        operator = get_operator(query_type)
        return operator(left, right)

def get_operator(query_type):
    operator_mapping = {
        'exact': operator.eq,
        'lte': operator.le,
        'gte': operator.ge,
        'lt': operator.lt,
        'gt': operator.gt,
    }
    try:
        return operator_mapping[query_type]
    except:
        raise ValueError('Unknown query type: {}'.format(query_type))


def create_static_entities():
    return {
        Student: EntityMapping(),
        TaskSession: EntityMapping(),
        Task: EntityMapping.from_list(TASKS),
    }

# TODO: move to some utils
def get_id(entity):
    return getattr(entity, get_id_field_name(entity))

def get_id_field_name(entity):
    return entity.__class__.__name__.lower() + '_id'


STATIC_ENTITIES = create_static_entities()
