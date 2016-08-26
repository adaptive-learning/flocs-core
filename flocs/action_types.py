"""Specify all available action types

Creates enum of available action types dynamically from all action creators
"""
from enum import Enum
from .action_creators import ALL_ACTION_TYPES
ActionType = Enum('ActionType', type=str,
                  names=[(name, name) for name in ALL_ACTION_TYPES])
