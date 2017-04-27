""" All available instructions
"""
from ..entities import Instruction

# pylint:disable=line-too-long
# pylint:disable=bad-whitespace
instructions = (
    Instruction(instruction_id='env.space-world'),
    Instruction(instruction_id='env.toolbox'),
    Instruction(instruction_id='env.snapping'),
    Instruction(instruction_id='env.controls'),
    Instruction(instruction_id='object.asteroid'),
    Instruction(instruction_id='object.meteoroid'),
    Instruction(instruction_id='object.diamond'),
    Instruction(instruction_id='object.wormhole'),
    Instruction(instruction_id='diamonds-status'),
    Instruction(instruction_id='energy-status'),
    Instruction(instruction_id='length-limit'),
    Instruction(instruction_id='block.fly'),
    Instruction(instruction_id='block.shoot'),
    Instruction(instruction_id='block.repeat'),
    Instruction(instruction_id='block.while'),
    Instruction(instruction_id='block.color'),
    Instruction(instruction_id='block.position'),
    Instruction(instruction_id='block.if'),
    Instruction(instruction_id='block.if-else'),
)
