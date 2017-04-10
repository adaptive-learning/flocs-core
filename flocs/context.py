""" Context is a part of the world state changing (potentially) continuously
"""
from datetime import datetime, timedelta
from itertools import count
from random import randint
from uuid import uuid4
from pyrsistent import PClass, field
from flocs import __version__


class Context(PClass):
    """ Base class providing context like time and randomness seed

    Attributes:
        - version: flocs version string
        - time: current datetime
        - randomness: seed for randomized algorithms
        - new_id: number or 'uuid' or 'seq'
    """
    default_time = datetime(1, 1, 1)

    version = __version__
    time = field(initial=default_time)
    randomness = field(initial=0)
    new_id = field(initial=0)

    @property
    def snapshot(self):
        return self


class DynamicContext:
    """ Dynamic context
    """
    def __init__(self):
        self.version = __version__
        self.new_id = 'uuid'

    @property
    def time(self):
        return datetime.now()

    @property
    def randomness(self):
        return randint(a=0, b=2**30)

    @property
    def snapshot(self):
        return Context(time=self.time, randomness=self.randomness, new_id=self.new_id)


class SimulationContext:
    """ Mutable simulation context
    """
    def __init__(self, time=datetime(1, 1, 1, 0, 0, 0), randomness=0, new_id='seq'):
        self.version = __version__
        self.time = time
        self.randomness = randomness
        self.new_id = new_id

    @property
    def snapshot(self):
        return Context(time=self.time, randomness=self.randomness, new_id=self.new_id)


static = Context()
dynamic = DynamicContext()


#def is_context(instance):
#    return all(hasattr(instance, attr) for attr in ['version', 'time', 'randomness', 'new_id'])


#def static(time=Context.default_time, randomness=0, new_id='seq'):
#    return Context(time=time, randomness=randomness, new_id=new_id)


#def dynamic():
#    context = Context(
#        time=datetime.now(),
#        randomness=randint(a=0, b=2**30),
#        new_id='uuid',
#    )
#    return context


def generate_id_if_not_set(maybe_id, generator=uuid4):
    just_id = maybe_id if maybe_id is not None else generator()
    return just_id
