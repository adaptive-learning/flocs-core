"""Unit tests for state
"""
from collections import namedtuple
import pytest
from flocs import state
from flocs.entities import Student, Task, TaskSession
from flocs.data.tasks import TASKS
from flocs.state import EntityMapping


def test_create_static_entities():
    created_entities = state.create_static_entities()
    expected_entities = {
        Student: {},
        Task: state.create_tasks_dict(),
        TaskSession: {},
    }
    assert created_entities == expected_entities


def test_create_tasks_dict():
    expected = {task.task_id: task for task in TASKS}
    created = state.create_tasks_dict()
    assert expected == created


class TestEntityMapping:
    entity_mapping_class = EntityMapping

    def test_getitem(self):
        entity_mapping = self.entity_mapping_class({'i': 'e'})
        assert entity_mapping['i'] == 'e'

    def test_get_nonexistent_item(self):
        entity_mapping = self.entity_mapping_class()
        with pytest.raises(KeyError):
            # pylint:disable=pointless-statement
            entity_mapping['i']

    def test_len(self):
        entity_mapping = self.entity_mapping_class({'i1': 'e1', 'i2': 'e2'})
        assert len(entity_mapping) == 2

    def test_iter(self):
        entity_mapping = self.entity_mapping_class({'i1': 'e1', 'i2': 'e2'})
        assert set(iter(entity_mapping)) == {'i1', 'i2'}

    def test_filter(self):
        entity_class = namedtuple('Entity', ['a', 'b'])
        e1 = entity_class(a=1, b=1)
        e2 = entity_class(a=1, b=2)
        e3 = entity_class(a=2, b=1)
        entity_mapping = self.entity_mapping_class({'i': e1, 'j': e2, 'k': e3})
        assert entity_mapping.filter(a=1) == EntityMapping({'i': e1, 'j': e2})

    def test_filter_empty(self):
        entity_class = namedtuple('Entity', ['a', 'b'])
        e1 = entity_class(a=1, b=1)
        e2 = entity_class(a=1, b=2)
        e3 = entity_class(a=2, b=1)
        entity_mapping = self.entity_mapping_class({'i': e1, 'j': e2, 'k': e3})
        assert entity_mapping.filter(a=3) == EntityMapping()

    def test_filter_gte(self):
        entity_class = namedtuple('Entity', ['a'])
        e1 = entity_class(a=1)
        e2 = entity_class(a=2)
        e3 = entity_class(a=3)
        entity_mapping = self.entity_mapping_class({'i': e1, 'j': e2, 'k': e3})
        assert entity_mapping.filter(a__gte=2) == EntityMapping({'j': e2, 'k': e3})

    def test_filter_conjunction(self):
        entity_class = namedtuple('Entity', ['a', 'b'])
        e1 = entity_class(a=1, b=1)
        e2 = entity_class(a=1, b=2)
        e3 = entity_class(a=2, b=1)
        entity_mapping = self.entity_mapping_class({'i': e1, 'j': e2, 'k': e3})
        assert entity_mapping.filter(a=1, b=2) == EntityMapping({'j': e2})
