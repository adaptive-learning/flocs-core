"""Unit tests for state
"""
from collections import ChainMap, namedtuple
import pytest
from flocs.state import EntityMapping


class TestEntityMapping:
    entity_mapping_class = EntityMapping
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
        self.entity_mapping = EntityMapping.from_list([self.e1, self.e2, self.e3])

    def test_from_list(self):
        assert self.entity_mapping_class.from_list([self.e1, self.e2]).to_dict() \
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

    #def test_filter_empty(self):
    #    assert self.entity_mapping.filter(a=3) == self.entity_mapping_class()

    def test_filter_gte(self):
        assert self.entity_mapping.filter(a__gte=2) \
               == self.entity_mapping_class.from_list([self.e2])

    def test_filter_conjunction(self):
        assert self.entity_mapping.filter(a=1, b=2) \
               == self.entity_mapping_class.from_list([self.e3])

    def test_chaining(self):
        """Test of simple chaining using ChainMap.

        Note, however, that created chain map only provides
        collections.abc.Mapping, not filter method.
        """
        e3_updated = self.entity_class(entity_id='k', a=7, b=2)
        entity_mapping = ChainMap(
            self.entity_mapping_class.from_list([e3_updated]),
            self.entity_mapping_class.from_list([self.e1, self.e2, self.e3])
        )
        assert entity_mapping['k'] == e3_updated

    #def test_chaining_squashing(self):
    #    e3_updated = self.entity_class(entity_id='k', a=2, b=1)
    #    entity_mapping = self.entity_mapping_class(ChainMap(
    #        self.entity_mapping_class.from_list([e3_updated]),
    #        self.entity_mapping_class.from_list([self.e1, self.e2, self.e3])
    #    ))
    #    assert entity_mapping.filter(a=2) \
    #            == self.entity_mapping_class.from_list([self.e2, e3_updated])
    #    assert entity_mapping.filter(a=1) == self.entity_mapping_class.from_list([self.e1])
