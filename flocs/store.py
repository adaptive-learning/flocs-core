""" Wiring for state and reducers
"""
from functools import reduce
from flocs.reducers import WORLD_REDUCER


class Store:
    """ Wires a state with reducers which describes how the state changes
    """
    def __init__(self, initial_state, hooks=None):
        self.initial_state = initial_state
        # TODO: possibility to choose a state shape / related reducers
        self.reducer = WORLD_REDUCER
        self.actions = []
        self.hooks = hooks or self.Hooks()

    class Hooks:
        """Base class providing no-op behavior for all available hooks
        """
        def post_commit(self, state, diff):
            pass

    @property
    def state(self):
        return reduce(self.reducer, self.actions, self.initial_state)

    @property
    def diff(self):
        return compute_diff(self.initial_state, self.state)

    def stage_action(self, action):
        self.actions.append(action)

    def commit(self):
        """Squash all actions to create new initial state
        """
        diff = self.diff
        self.initial_state = self.state
        self.actions = []
        self.hooks.post_commit(state=self.state, diff=diff)

    @classmethod
    def open(self, state_creator, hooks=None):
        return StoreContextManager(state_creator, hooks)



def compute_diff(old_state, new_state):
    """ Return list of changes between the old and new state

    >>> old = {'entities.students': 'x', 'entitities.tasks': 'y'}
    >>> new = {'entities.students': 'z', 'entitities.tasks': 'y'}
    >>> compute_diff(old, new)
    [('entities.students', 'z')]
    """
    diff = [
        (key, new_value)
        for key, new_value in new_state.items()
        if new_value is not old_state[key]
    ]
    return diff


class StoreContextManager:
    def __init__(self, state_creator, hooks=None):
        self.store = None
        self.state_creator = state_creator
        self.hooks = hooks

    def __enter__(self):
        self.store = Store(initial_state=self.state_creator(), hooks=self.hooks)
        return self.store

    def __exit__(self, exc_type, exc_value, traceback):
        self.store.commit()
