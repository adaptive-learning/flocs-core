"""
Representation of a world state
"""
from collections import namedtuple, UserDict
from datetime import datetime
from flocs import data, __version__


class State(UserDict):
    """ World state representation.

    Allows for LazyValues which will be evaluated on demand.
    """
    def __init__(self, initial_data=None):
        provided_initial_data = initial_data or {}
        complete_initial_data = {**EMPTY_STATE_DATA, **provided_initial_data}
        super().__init__(complete_initial_data)

    def __getitem__(self, key):
        value = self.data[key]
        if isinstance(value, LazyValue):
            value = value.fn()
            self.data[key] = value
        return value


LazyValue = namedtuple('LazyValue', ['fn'])


EMPTY_STATE_DATA = {
    'meta.version': __version__,
    'entities.tasks': data.TASKS,
    'entities.students': {},
    'entities.task_instances': {},
    'context.time': datetime(1, 1, 1),
    'context.randomness_seed': 0,
    }
