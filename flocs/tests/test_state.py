"""Unit tests for state
"""
from collections import namedtuple
import pytest
from flocs.state import EntityMapping


class TestEntityMapping:
    entity_mapping_class = EntityMapping
    entity_class = namedtuple('Entity', ['entity_id', 'a', 'b'])

    def test_from_list(self):
        e1 = self.entity_class(entity_id=1, a=1, b=1)
        e2 = self.entity_class(entity_id=2, a=1, b=1)
        entity_mapping = self.entity_mapping_class.from_list([e1, e2])
        assert entity_mapping == EntityMapping({1: e1, 2: e2})

    def test_getitem(self):
        entity_mapping = self.entity_mapping_class({'i': 'e'})
        assert entity_mapping['i'] == 'e'

    def test_get_nonexistent_item(self):
        entity_mapping = self.entity_mapping_class()
        with pytest.raises(KeyError):
            # pylint:disable=pointless-statement
            entity_mapping['i']

    def test_len(self):
        entity_mapping = self.entity_mapping_class({'i': 'e', 'j': 'f'})
        assert len(entity_mapping) == 2

    def test_iter(self):
        entity_mapping = self.entity_mapping_class({'i': 'e', 'j': 'f'})
        assert set(iter(entity_mapping)) == {'i', 'j'}

    def test_filter(self):
        e1 = self.entity_class(entity_id=1, a=1, b=1)
        e2 = self.entity_class(entity_id=2, a=1, b=1)
        e3 = self.entity_class(entity_id=3, a=2, b=1)
        entity_mapping = self.entity_mapping_class.from_list([e1, e2, e3])
        assert entity_mapping.filter(a=1) == self.entity_mapping_class.from_list([e1, e2])

    def test_filter_empty(self):
        e1 = self.entity_class(entity_id=1, a=1, b=1)
        e2 = self.entity_class(entity_id=2, a=1, b=1)
        e3 = self.entity_class(entity_id=3, a=2, b=1)
        entity_mapping = self.entity_mapping_class.from_list([e1, e2, e3])
        assert entity_mapping.filter(a=3) == self.entity_mapping_class()

    def test_filter_gte(self):
        e1 = self.entity_class(entity_id=1, a=1, b=1)
        e2 = self.entity_class(entity_id=2, a=2, b=1)
        e3 = self.entity_class(entity_id=3, a=3, b=1)
        entity_mapping = self.entity_mapping_class.from_list([e1, e2, e3])
        assert entity_mapping.filter(a__gte=2) == self.entity_mapping_class.from_list([e2, e3])

    def test_filter_conjunction(self):
        e1 = self.entity_class(entity_id=1, a=1, b=1)
        e2 = self.entity_class(entity_id=2, a=1, b=2)
        e3 = self.entity_class(entity_id=3, a=2, b=1)
        entity_mapping = self.entity_mapping_class.from_list([e1, e2, e3])
        assert entity_mapping.filter(a=1, b=2) == self.entity_mapping_class.from_list([e2])
