import pytest
from collections import ChainMap
from flocs.entities import Student, TaskInstance
from flocs.state import STATIC_ENTITIES
from flocs.tests.fixtures_task_instances import *


@pytest.fixture
def entities_00():
    return STATIC_ENTITIES


@pytest.fixture
def entities_01():
    new_entities = {
        TaskInstance: task_instances_00()
    }
    return ChainMap(new_entities, entities_00())


@pytest.fixture
def entities_02():
    new_entities = {
        TaskInstance: task_instances_02(),
    }
    return ChainMap(new_entities, entities_00())


@pytest.fixture
def entities_03():
    new_entities = {
        TaskInstance: task_instances_01()
    }
    return ChainMap(new_entities, entities_00())


