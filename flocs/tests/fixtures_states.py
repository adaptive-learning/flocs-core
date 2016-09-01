"""
Some worldstates for testing purposes
"""
from collections import ChainMap
import pytest
from flocs.tests.fixtures_entities import *
from flocs.state import State
from flocs.context import STATIC_CONTEXT


@pytest.fixture
def state_00():
    return State.create(
        entities=entities_00(),
        context=STATIC_CONTEXT,
    )


@pytest.fixture
def state_01():
    return State.create(
        entities=entities_01(),
        context=STATIC_CONTEXT,
    )


@pytest.fixture
def state_02():
    return State.create(
        entities=entities_02(),
        context=STATIC_CONTEXT,
    )
