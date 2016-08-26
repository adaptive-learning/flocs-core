""" Actions represent events and interactions in the world we want to model
"""
from collections import namedtuple
from enum import Enum


Action = namedtuple('Action', [
    'type',     # one of the string from the finite set of actions (ActionType enum)
    'data',     # dictionary of data specific to this action
    'context',  # optionally specified context (part of state changing continuously, e.g. time
    'meta'      # optionally specified mata-information, such as package version
    ])


_action_types = set()
def action_creator(action_data_creator):
    """Decorate function to make it an action creator
    >>> @action_creator
    ... def create_fruit(fruit_id=None, context=None):
    ...     fruit_id = fruit_id if fruit_id is not None else context['magic']
    ...     return {'fruit_id': fruit_id}
    >>> create_fruit(fruit_id=None, context={'magic': 16}, meta={})
    Action(type='create_fruit', data={'fruit_id': 16}, context={'magic': 16}, meta={})
    """
    action_type = action_data_creator.__name__
    _action_types.add(action_type)
    def wrapped_action_creator(*args, context=None, meta=None, **kwargs):
        data = action_data_creator(*args, context=context, **kwargs)
        return Action(type=action_type, data=data, context=context, meta=meta)
    return wrapped_action_creator


def get_registered_action_types():
    return _action_types
