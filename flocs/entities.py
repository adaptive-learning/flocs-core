""" Type definitions for domain entities
"""
from collections import namedtuple



class Action(namedtuple('Action', ['action_id', 'type', 'data',
                                   'time', 'randomness', 'version'])):
    """ Describes an atomic event in the world we model
    """
    __slots__ = ()

    def add_context(self, context):
        action_with_context = self._replace(
            time=context.time,
            randomness=context.randomness,
            version=context.version)
        return action_with_context


Student = namedtuple('Student', [
    'student_id',
    'last_task_session_id',
    'credits'
])


SeenInstruction = namedtuple('SeenInstruction', [
    'seen_instruction_id',
    'student_id',
    'instruction_id',
])


Task = namedtuple('Task', [
    'task_id',
    'category_id',
    'setting',
    'solution',
])


Category = namedtuple('Category', [
    'category_id',
    'level_id',
    'toolbox_id',
])


Level = namedtuple('level', [
    'level_id',
    'credits',
])


Toolbox = namedtuple('Toolbox', [
    'toolbox_id',
    'block_ids',
])


Block = namedtuple('Block', [
    'block_id',
])


class TaskSession(namedtuple('TaskSession', [
        'task_session_id', 'student_id', 'task_id',
        'solved', 'given_up',
        'time_start', 'time_end'])):
    __slots__ = ()

    def __new__(cls, task_session_id=None, student_id=None, task_id=None,
                     solved=False, given_up=False, time_start=None, time_end=None):
        return super().__new__(cls,
            task_session_id=task_session_id,
            student_id=student_id,
            task_id=task_id,
            solved=solved,
            given_up=given_up,
            time_start=time_start,
            time_end=time_end)

    @property
    def time_spent(self):
        return self.time_end - self.time_start


Instruction = namedtuple('Instruction', [
    'instruction_id',
])


#Concept = namedtuple('Concept', [
#    'concept_id',
#    'ref',
#    'subconcepts',
#])
#
#
#ActivityRecommendation = namedtuple('ActivityRecommendation', [
#    'activity_recommendation_id',
#    'student_id',
#    'activity',
#])
#
#
#TaskRecommendation = namedtuple('TaskRecommendation', [
#    'task_recommendation_id',
#    'student_id',
#    'task_id',
#])
