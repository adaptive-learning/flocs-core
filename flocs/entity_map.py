import operator
from collections import ChainMap
from collections.abc import Mapping
from .utils.names import camel_to_snake_case


class EntityMap(Mapping):
    """ Collection of all entities of given type (i.e., 1 entity table)
    """
    def __init__(self, *maps, state=None, ordering=None):
        """ Initialize with provided map(s)
            Reference to state is only needed for complex filtering tasks that
            uses entities of other types
        """
        self.chain_map = ChainMap(*maps)
        self.ordering = ordering
        self.state = state

    @classmethod
    def from_list(cls, entity_list):
        return cls({get_id(entity): entity for entity in entity_list})

    def __getitem__(self, entity_id):
        return self.chain_map[entity_id]

    def __iter__(self):
        if self.ordering is None:
            return iter(self.chain_map)
        key = lambda pk: getattr(self[pk], self.ordering)
        return iter(sorted(self.chain_map, key=key))

    def __len__(self):
        return len(self.chain_map)

    def __repr__(self):
        return 'EntityMap({data})'.format(data=self.chain_map)

    def __str__(self):
        if len(self) == 0:
            return 'Empty EntityMap'
        msg = '{entity_class} entities:\n{entities}'.format(
            entity_class=self.entity_class.__name__,
            entities='\n'.join('* ' + str(e) for e in self.values()))
        return msg

    @property
    def entity_class(self):
        try:
            entity = next(iter(self.values()))
            return entity.__class__
        except StopIteration:
            return None

    def set(self, entity):
        """ Return a new map from self and the given entity
        It effectively updates entity if exists, creates otherwise.
        """
        entity_id = get_id(entity)
        return EntityMap({entity_id: entity}, *self.chain_map.maps)

    @property
    def original_entities(self):
        # if there was no modification, return self - this allows to perform
        # diffing in constant time by comparing references
        return self if len(self.chain_map.maps) == 1 else self.chain_map.maps[-1]

    @property
    def modified_entities(self):
        """ Return entities which were set since the original state
        """
        return ChainMap(*self.chain_map.maps[:-1])

    def exists(self):
        """ Return True iff there is at least 1 entity in the map
        """
        return len(self) >= 1

    def filter(self, **kwargs):
        """ Return a new map filtered according to given query given by kwargs

        For full kwargs specification, see Django QuerySet's filter:
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups
        But only a subset of lookups is currently implemented, see _test_entity_single

        Note that filtering works even with many maps, but beware that it's
        iterating through all element, even if some nested map has another
        (more efficient) implementation of filter method.
        """
        # if len(self.chain_map.maps) != 1:
        #     raise ValueError('Filtering only supported for initial (unmodified) maps')
        filtered_dict = {
            entity_id: entity
            for entity_id, entity in self.items()
            if self._test_entity(entity, **kwargs)
        }
        return EntityMap(filtered_dict)

    def order_by(self, field):
        return EntityMap(self, ordering=field)

    def first(self):
        try:
            return next(iter(self.values()))
        except StopIteration:
            return None

    def last(self):
        try:
            return list(self.values())[-1]
        except IndexError:
            return None

    def _test_entity(self, entity, **kwargs):
        """ Return True if a given entity satisfies condition by **kwargs
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


# TODO: move to some utils
def get_id(entity):
    return getattr(entity, get_id_field_name(entity))


def get_id_field_name(entity):
    class_name = entity.__class__.__name__
    id_field_name = camel_to_snake_case(class_name) + '_id'
    return id_field_name
