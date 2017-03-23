"""Unit tests for context
"""

from datetime import datetime, timedelta
from random import randint
from flocs.context import dynamic, Context, StaticContext, SimulationContext
from flocs.context import generate_id_if_not_set

class TestContext:
    context = Context()

    def test_context_interface(self):
        assert hasattr(self.context, 'version')
        assert hasattr(self.context, 'time')
        assert hasattr(self.context, 'randomness')
        assert hasattr(self.context, 'new_id')


class TestDynamicContext(TestContext):
    context = dynamic


class TestStaticContext(TestContext):
    context = StaticContext()

    def test_fixed_randomness(self):
        assert self.context.randomness == self.context.randomness

    def test_fixed_time(self):
        assert self.context.time == self.context.time

    def test_new_id_sequence(self):
        assert self.context.new_id() == 0
        assert self.context.new_id() == 1
        assert self.context.new_id() == 2


class TestSimulationContext(TestContext):
    context = SimulationContext(
        randomness=4,
        initial_time=datetime(1, 2, 3, 0, 55, 0),
        time_step=timedelta(minutes=10))

    def test_fixed_randomness(self):
        assert self.context.randomness == 4
        assert self.context.randomness == 4

    def test_simulation_time(self):
        t1 = self.context.time
        t2 = self.context.time
        assert t2 - t1 == timedelta(minutes=10)


def test_generate_id_if_not_set_when_set():
    generated_id = generate_id_if_not_set(55)
    assert generated_id == 55


def test_generate_id_if_not_set_when_not_set():
    generator = lambda: 817
    generated_id = generate_id_if_not_set(None, generator=generator)
    assert generated_id == 817
