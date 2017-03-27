"""Context is a part of the world state changing (potentially) continuously
"""
from datetime import datetime, timedelta
from itertools import count
from random import randint
from uuid import uuid4
from flocs import __version__


class Context:
    """ Base class providing (potentially dynamic) context like time and new IDs

    Attributes:
        - version
        - time
        - randomness

    Methods:
        - new_id
    """
    def __init__(self):
        self.version = __version__

    @property
    def time(self):
        return datetime.now()

    @property
    def randomness(self):
        return randint(a=0, b=2**30)

    def new_id(self):
        return uuid4()


class StaticContext(Context):
    """ Static context for tests with non-changing time
    """
    default_time = datetime(1, 1, 1)

    def __init__(self, time=default_time, randomness=0, new_id=0):
        super().__init__()
        self._time = time
        self._randomness = randomness
        self._new_id = new_id

    @property
    def time(self):
        return self._time

    @property
    def randomness(self):
        return self._randomness

    def new_id(self):
        return self._new_id



class SimulationContext(StaticContext):
    """ Context for simulations which allows to set initial time and time step
    """
    def __init__(self,
                 randomness=0,
                 initial_time=datetime(1, 1, 1, 0, 0, 0),
                 time_step=timedelta(minutes=1)):
        super().__init__()
        self._time_step = time_step
        self._next_time = initial_time
        self._randomness = randomness
        self._id_generator = count()

    @property
    def time(self):
        current_time = self._next_time
        self._next_time += self._time_step
        return current_time

    @property
    def randomness(self):
        return self._randomness

    def new_id(self):
        return next(self._id_generator)


def generate_id_if_not_set(maybe_id, generator=uuid4):
    just_id = maybe_id if maybe_id is not None else generator()
    return just_id


# default immutable context instances
dynamic = Context()
static = StaticContext()
