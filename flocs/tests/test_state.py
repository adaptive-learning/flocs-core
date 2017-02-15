"""Unit tests for state
"""
from collections import ChainMap, namedtuple
import pytest
from flocs.state import EntityMap


class TestEntityMap:
    entity_mapping_class = EntityMap
    entity_class = namedtuple('Entity', ['entity_id', 'a', 'b'])

    #def __init__(self):
    #    self.e1 = None
    #    self.e2 = None
    #    self.e3 = None
    #    self.entity_mapping = None

    def setup_method(self, method):
        self.e1 = self.entity_class(entity_id='i', a=1, b=1)
        self.e2 = self.entity_class(entity_id='j', a=2, b=1)
        self.e3 = self.entity_class(entity_id='k', a=1, b=2)
        self.entity_mapping = EntityMap.from_list([self.e1, self.e2, self.e3])

    def test_from_list(self):
        assert dict(self.entity_mapping_class.from_list([self.e1, self.e2])) \
            == {'i': self.e1, 'j': self.e2}

    def test_getitem(self):
        assert self.entity_mapping['i'] == self.e1

    def test_get_nonexistent_item(self):
        with pytest.raises(KeyError):
            # pylint:disable=pointless-statement
            self.entity_mapping['aaa']

    def test_len(self):
        assert len(self.entity_mapping) == 3

    def test_iter(self):
        assert set(iter(self.entity_mapping)) == {'i', 'j', 'k'}

    def test_filter(self):
        assert self.entity_mapping.filter(a=1) \
               == self.entity_mapping_class.from_list([self.e1, self.e3])

    def test_filter_empty(self):
        assert self.entity_mapping.filter(a=3) == self.entity_mapping_class()

    def test_filter_gte(self):
        assert self.entity_mapping.filter(a__gte=2) \
               == self.entity_mapping_class.from_list([self.e2])

    def test_filter_conjunction(self):
        assert self.entity_mapping.filter(a=1, b=2) \
               == self.entity_mapping_class.from_list([self.e3])

    def test_set_new(self):
        e4 = self.entity_class(entity_id='l', a=1, b=1)
        em_updated = self.entity_mapping.set(e4)
        em_expected = self.entity_mapping_class.from_list([self.e1, self.e2, self.e3, e4])
        assert em_updated == em_expected

    def test_set_existing(self):
        e3_updated = self.entity_class(entity_id='k', a=7, b=2)
        em_updated = self.entity_mapping.set(e3_updated)
        em_expected = self.entity_mapping_class.from_list([self.e1, self.e2, e3_updated])
        assert em_updated == em_expected

    def test_entity_class_property(self):
        assert self.entity_mapping.entity_class == self.entity_class
