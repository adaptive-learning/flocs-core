""" Type definitions for domain entities
"""
from collections import namedtuple


Student = namedtuple('Student', [
    'student_id',
    'last_task_session',
])


Task = namedtuple('Task', [
    'task_id',
    'setting',
    'solution',
])


TaskSession = namedtuple('TaskSession', [
    'task_session_id',
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
    'subconcepts',
])


Toolbox = namedtuple('Toolbox', [
    'toolbox_id',
    'ref',
    'blocks_refs',
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
