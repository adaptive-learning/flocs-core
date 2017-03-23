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

    def new_id(self):
        return uuid4()

    @property
    def time(self):
        return datetime.now()

    @property
    def randomness(self):
        return randint(a=0, b=2**30)


class StaticContext(Context):
    """ Static context for tests with non-changing time
    """
    fixed_time = datetime(1, 1, 1)
    fixed_randomness = 0

    def __init__(self):
        super().__init__()
        self._id_generator = count()

    def new_id(self):
        return next(self._id_generator)

    @property
    def time(self):
        return self.fixed_time

    @property
    def randomness(self):
        return self.fixed_randomness



class SimulationContext(StaticContext):
    """ Context for simulations which allows to set initial time and time step
    """
    def __init__(self,
                 randomness=0,
                 initial_time=datetime(1, 1, 1, 0, 0, 0),
                 time_step=timedelta(minutes=1)):
        super().__init__()
        self._time_step = time_step
        self._time = initial_time
        self._randomness = randomness

    @property
    def time(self):
        self._time += self._time_step
        return self._time

    @property
    def randomness(self):
        return self._randomness


def generate_id_if_not_set(maybe_id, generator=uuid4):
    just_id = maybe_id if maybe_id is not None else generator()
    return just_id


# default dynamic context instance
dynamic = Context()
