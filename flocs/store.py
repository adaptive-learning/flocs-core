"""World state and behavior (wiring for state and reducers)
"""
from contextlib import contextmanager
from functools import reduce
from flocs.reducers import reduce_state
from flocs.state import create_state


class Store:
    """Represents state of the world together with its behavior
    """
    def __init__(self, entities, create_context, hooks=None):
        self.create_context = create_context
        self.initial_state = create_state(entities, self.context)
        self.actions = []
        self.hooks = hooks or self.Hooks()

    class Hooks:
        """Base class providing no-op behavior for all available hooks
        """
        def post_commit(self, state, diff, actions):
            pass

    @property
    def context(self):
        return self.create_context()

    @property
    def state(self):
        return reduce(reduce_state, self.actions, self.initial_state)

    def compute_diff(self):
        return compute_diff(self.initial_state, self.state)

    def stage_action(self, action):
        self.actions.append(action)

    def commit(self):
        """Squash all actions to create new initial state
        """
        diff = self.compute_diff()
        actions = self.actions
        self.initial_state = self.state
        self.actions = []
        self.hooks.post_commit(state=self.state, diff=diff, actions=actions)

    @contextmanager
    @classmethod
    def open(cls, entities, create_context, hooks=None):
        store = cls(entities=entities, create_context=create_context, hooks=hooks)
        yield store
        store.commit()


def compute_diff(old_state, new_state):
    return compute_entities_diff(old_state.entities, new_state.entities)


def compute_entities_diff(old, new):
    """Return list of changes between the old and new entities

    >>> old = {'students': {1: 'a', 2: 'b'}, 'tasks': {1: 'x'}}
    >>> new = {'students': {1: 'a', 2: 'B'}, 'tasks': {2: 'y'}}
    >>> sorted(compute_entities_diff(old, new))
    [('students', 2, 'B'), ('tasks', 1, None), ('tasks', 2, 'y')]
    """
    diff = [
        (entity_name, entity_id, new[entity_name].get(entity_id, None))
        for entity_name in new
        for entity_id in old[entity_name].keys() | new[entity_name].keys()
        if new[entity_name].get(entity_id, None) is not old[entity_name].get(entity_id, None)
    ]
    return diff
