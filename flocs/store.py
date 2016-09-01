"""World state and behavior (wiring for state and reducers)
"""
from contextlib import contextmanager
from functools import reduce
from .context import default_context_generator
from .reducers import reduce_state
from .state import State


class Store:
    """Represents state of the world together with its behavior

    State si changing due to time (context) and actions (entities),
    store describes how the state evolves and how it looks right now
    """
    def __init__(self, entities=None, context_generator=default_context_generator, hooks=None):
        self.context_generator = context_generator()
        self.initial_state = State.create(
            entities=entities or {},
            context=self.current_context
        )
        self.actions = []
        self.hooks = hooks or self.Hooks()

    class Hooks:
        """Base class providing no-op behavior for all available hooks
        """
        def post_commit(self, state, diff, actions):
            pass

    @property
    def current_context(self):
        return next(self.context_generator)

    @property
    def state(self):
        state_after_last_action = reduce(reduce_state, self.actions, self.initial_state)
        current_state = state_after_last_action._replace(context=self.current_context)
        return current_state

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

    @classmethod
    @contextmanager
    def open(cls, *args, **kwargs):
        store = cls(*args, **kwargs)
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
