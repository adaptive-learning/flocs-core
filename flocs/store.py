"""World state and behavior (wiring for state and reducers)
"""
from contextlib import contextmanager
from functools import reduce
from .context import dynamic
from .reducers import reduce_state
from .state import State


class Store:
    """Represents state of the world together with its behavior

    State is changing due to time (context) and actions (entities),
    store describes how the state evolves and how it looks right now
    """
    def __init__(self, entities=None, context=dynamic, hooks=None):
        self.context = context
        self.initial_state = State(
            entities=entities or {},
            time=context.time,
            randomness=context.randomness,
            version=context.version,
        )
        self.actions = []
        self.hooks = hooks or self.Hooks()

    class Hooks:
        """Base class providing no-op behavior for all available hooks
        """
        # more hook points expected in the future
        # pylint:disable=too-few-public-methods
        def post_commit(self, state, diff):
            pass

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
        self.initial_state = self.state
        self.actions = []
        self.hooks.post_commit(state=self.state, diff=diff)

    @classmethod
    @contextmanager
    def open(cls, *args, **kwargs):
        store = cls(*args, **kwargs)
        yield store
        store.commit()


def compute_diff(old_state, new_state):
    return compute_entities_diff(old_state.entities, new_state.entities)


def compute_entities_diff(old_entities, new_entities):
    """ Return list of changes between the old and new entities
    """
    # TODO: refactor to make it more readable and easily testable
    diff = []
    for entity_class, entity_map in new_entities.items():
        if entity_map.original_entities is old_entities[entity_class]:
            diff.extend(
                (entity_class, entity_id, new_entity)
                for entity_id, new_entity in entity_map.modified_entities.items()
            )
        else:
            diff.extend(
                (entity_class, entity_id, entity_map.get(entity_id, None))
                for entity_id in entity_map.keys() | old_entities[entity_class].keys()
                if entity_map.get(entity_id, None) \
                   is not old_entities[entity_class].get(entity_id, None)
            )
    return diff
