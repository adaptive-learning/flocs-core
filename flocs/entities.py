""" Type definitions for domain entities
"""
from collections import namedtuple


Student = namedtuple('Student', [
    'student_id',
])


Task = namedtuple('Task', [
    'task_id',
    'ref',
])


TaskInstance = namedtuple('TaskInstance', [
    'task_instance_id',
    'student_id',
    'task_id',
    'solved',
    'given_up',
])


TaskStats = namedtuple('TaskStats', [
    'task_id',
    'started_count',
    'solved_count',
    'given_up_count',
])


Concept = namedtuple('Concept', [
    'concept_id',
    'ref',
    'type',
])


Toolbox = namedtuple('Toolbox', [
    'toolbox_id',
    'ref',
    'blocks_ids',
])


Block = namedtuple('Block', [
    'block_id',
    'ref',
])


Instruction = namedtuple('Instruction', [
    'instruction_id',
    'concept_id',
    'ref',
])


ActivityRecommendation = namedtuple('ActivityRecommendation', [
    'activity_recommendation_id',
    'student_id',
    'activity',
])


TaskRecommendation = namedtuple('TaskRecommendation', [
    'task_recommendation_id',
    'student_id',
    'task_id',
])
