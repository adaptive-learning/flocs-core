"""Available concepts
"""
from ..entities import Concept

# pylint:disable=line-too-long

CONCEPTS = (
    Concept(concept_id=1, ref='programming', subconcepts=['programming_sequence', 'programming_loops']),
    Concept(concept_id=2, ref='blockly', subconcepts=['block_spaceship_move', 'block_repeat']),
    Concept(concept_id=3, ref='environment', subconcepts=[]),
    Concept(concept_id=4, ref='spaceship', subconcepts=[]),
    Concept(concept_id=5, ref='block_spaceship_move', subconcepts=[]),
    Concept(concept_id=6, ref='block_repeat', subconcepts=[]),
    Concept(concept_id=7, ref='programming_sequence', subconcepts=[]),
    Concept(concept_id=8, ref='programming_loops', subconcepts=[]),
)
