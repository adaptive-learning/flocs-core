"""Unit tests for context
"""

from datetime import datetime, timedelta
import pytest
from flocs.context import static, dynamic, Context, SimulationContext
from flocs.context import generate_id_if_not_set

class TestContext:
    context = Context()

    def test_context_interface(self):
        assert hasattr(self.context, 'version')
        assert hasattr(self.context, 'time')
        assert hasattr(self.context, 'randomness')
        assert hasattr(self.context, 'new_id')
        assert hasattr(self.context, 'snapshot')

    def test_snapshot_returns_context(self):
        assert isinstance(self.context.snapshot, Context)


class TestDynamicContext(TestContext):
    context = dynamic


class TestStaticContext(TestContext):
    context = static

    def test_fixed_randomness(self):
        assert self.context.randomness == self.context.randomness

    def test_fixed_time(self):
        assert self.context.time == self.context.time

    def test_fixed_new_id(self):
        assert self.context.new_id == self.context.new_id == 0

    def test_immutability(self):
        with pytest.raises(AttributeError):
            static.randomness = 4

    def test_snapshot(self):
        assert static.snapshot == static


class TestContextWithParameters(TestContext):
    context = Context(time=0, randomness=1, new_id=2)

    def test_fixed_time(self):
        assert self.context.time == 0
        assert self.context.time == 0

    def test_fixed_randomness(self):
        assert self.context.randomness == 1
        assert self.context.randomness == 1

    def test_fixed_new_id(self):
        assert self.context.new_id == 2
        assert self.context.new_id == 2

    def test_snapshot(self):
        assert self.context.snapshot == Context(time=0, randomness=1, new_id=2)


class TestSimulationContext(TestContext):
    context = SimulationContext(randomness=4, time=datetime(1, 2, 3, 0, 55, 0))

    def test_fixed_randomness(self):
        assert self.context.randomness == 4
        assert self.context.randomness == 4

    def test_simulation_time(self):
        t1 = self.context.time
        assert t1 == datetime(1, 2, 3, 0, 55, 0)
        self.context.time += timedelta(hours=10)
        t2 = self.context.time
        assert t2 == datetime(1, 2, 3, 10, 55, 0)


def test_generate_id_if_not_set_when_set():
    generated_id = generate_id_if_not_set(55)
    assert generated_id == 55


def test_generate_id_if_not_set_when_not_set():
    generator = lambda: 817
    generated_id = generate_id_if_not_set(None, generator=generator)
    assert generated_id == 817
