""" Wiring for state and reducers
"""
from functools import reduce


class Store:
    """ Wires a state with reducers which describes how the state changes
    """
    def __init__(self, initial_state, reducer):
        self.initial_state = initial_state
        self.reducer = reducer
        self.actions = []

    @property
    def state(self):
        return reduce(self.reducer, self.actions, self.initial_state)

    def stage_action(self, action):
        self.actions.append(action)

    def commit(self):
        pass # TODO: update state by applying all staged actions
