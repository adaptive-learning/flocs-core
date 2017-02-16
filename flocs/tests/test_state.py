"""Unit tests for state
"""
from collections import namedtuple
import pytest
from flocs.state import EntityMap

# simple entity class for testing and a few instances
Entity = namedtuple('Entity', ['entity_id', 'a', 'b'])
e1 = Entity(entity_id='i', a=1, b=1)
e2 = Entity(entity_id='j', a=2, b=1)
e3 = Entity(entity_id='k', a=1, b=2)

# pylint:disable=unused-argument
# pylint:disable=attribute-defined-outside-init
# pylint:disable=pointless-statement
class TestEntityMap:

    @staticmethod
    def create_entity_map(*entities):
        """ Factory method to create an instance of any class providing
            EntityMap interface you want to test
        """
        return EntityMap.from_list(entities)

    #def setup_method(self, method):
    #    pass

    def test_getitem(self):
        entity_map = self.create_entity_map(e1, e2, e3)
        assert entity_map['j'] == e2

    def test_get_nonexistent_item(self):
        entity_map = self.create_entity_map(e1, e2)
        with pytest.raises(KeyError):
            entity_map['k']

    def test_len(self):
        entity_map = self.create_entity_map(e1, e2, e3)
        assert len(entity_map) == 3

    def test_iter(self):
        entity_map = self.create_entity_map(e1, e2, e3)
        assert set(iter(entity_map)) == {'i', 'j', 'k'}

    def test_dict(self):
        entity_map = self.create_entity_map(e1, e2)
        assert dict(entity_map) == {'i': e1, 'j': e2}

    def test_filter(self):
        entity_map = self.create_entity_map(e1, e2, e3).filter(a=1)
        assert entity_map == self.create_entity_map(e1, e3)
        #assert dict(entity_map) == {'i': e1, 'k': e3}

    def test_filter_empty(self):
        entity_map = self.create_entity_map(e1, e2, e3).filter(a=100)
        assert entity_map == self.create_entity_map()

    def test_filter_gte(self):
        entity_map = self.create_entity_map(e1, e2, e3).filter(a__gte=2)
        assert entity_map == self.create_entity_map(e2)

    def test_filter_conjunction(self):
        entity_map = self.create_entity_map(e1, e2, e3).filter(a=1, b=2)
        assert entity_map == self.create_entity_map(e3)

    def test_set_check_structure(self):
        initial_entity_map = self.create_entity_map(e1, e2, e3)
        e4 = Entity(entity_id='l', a=1, b=1)
        updated_entity_map = initial_entity_map.set(e4)
        # set() is supposed to return EntityMap, not a subclass
        assert isinstance(updated_entity_map, EntityMap)
        assert len(updated_entity_map.chain_map.maps) == 2
        last_map = updated_entity_map.chain_map.maps[-1]
        assert last_map == initial_entity_map

    def test_set_new(self):
        entity_map = self.create_entity_map(e1, e2, e3)
        e4 = Entity(entity_id='l', a=1, b=1)
        em_updated = entity_map.set(e4)
        # set() is supposed to return EntityMap, not a subclass
        assert em_updated == EntityMap.from_list([e1, e2, e3, e4])

    def test_set_existing(self):
        entity_map = self.create_entity_map(e1, e2, e3)
        e3_updated = Entity(entity_id='k', a=7, b=2)
        em_updated = entity_map.set(e3_updated)
        # set() is supposed to return EntityMap, not a subclass
        assert em_updated == EntityMap.from_list([e1, e2, e3_updated])

    def test_set_chaining(self):
        e3_updated = Entity(entity_id='k', a=7, b=2)
        e4 = Entity(entity_id='l', a=1, b=1)
        entity_map = self.create_entity_map(e1, e2, e3).set(e3_updated).set(e4)
        assert entity_map == EntityMap.from_list([e1, e2, e3_updated, e4])

    def test_entity_class_property(self):
        entity_map = self.create_entity_map(e1, e2, e3)
        assert entity_map.entity_class == Entity
