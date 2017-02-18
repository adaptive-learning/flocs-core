""" All available toolboxes
"""
from ..entities import Toolbox

# pylint:disable=line-too-long
# pylint:disable=bad-whitespace
toolboxes = (
    Toolbox(toolbox_id='fly',               block_ids=['fly']),
    Toolbox(toolbox_id='shoot',             block_ids=['fly', 'shoot']),
    Toolbox(toolbox_id='repeat',            block_ids=['fly', 'shoot', 'repeat']),
    Toolbox(toolbox_id='while',             block_ids=['fly', 'shoot', 'while', 'color']),
    Toolbox(toolbox_id='loops',             block_ids=['fly', 'shoot', 'repeat', 'while', 'color']),
    Toolbox(toolbox_id='loops+if',          block_ids=['fly', 'shoot', 'repeat', 'while', 'color', 'if']),
    Toolbox(toolbox_id='loops+if+position', block_ids=['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if']),
    Toolbox(toolbox_id='loops+if+else',     block_ids=['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if', 'if-else']),
    Toolbox(toolbox_id='complete',          block_ids=['fly', 'shoot', 'repeat', 'while', 'color', 'position', 'if', 'if-else']),
)
