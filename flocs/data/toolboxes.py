"""Available toolboxes
"""
from ..entities import Toolbox


TOOLBOXES = (
    Toolbox(toolbox_id=1, ref='initial', blocks_refs=['spaceship_move']),
    Toolbox(toolbox_id=2, ref='repeat', blocks_refs=['spaceship_move', 'repeat']),
)
