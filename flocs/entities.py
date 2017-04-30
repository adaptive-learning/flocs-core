""" Type definitions for domain entities
"""
from collections import namedtuple
from datetime import timedelta
from .context import Context


class Action(namedtuple('Action', ['action_id', 'type', 'data',
                                   'time', 'randomness', 'version'])):
    """ Describes an atomic event in the world we model
    """
    __slots__ = ()

    def set_context(self, context):
        action_with_context = self._replace(
            time=context.time,
            randomness=context.randomness,
            version=context.version)
        return action_with_context

    @property
    def context(self):
        return Context(time=self.time, randomness=self.randomness)

    def _asdict(self):
        d = super()._asdict()
        d['data'] = dict(d['data'])
        return d


Session = namedtuple('Session', [
    'session_id',
    'student_id',
    'start',
    'end',
])


Student = namedtuple('Student', [
    'student_id',
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


Level = namedtuple('Level', [
    'level_id',
    'credits',
])


Toolbox = namedtuple('Toolbox', [
    'toolbox_id',
    'block_ids',
])


Block = namedtuple('Block', [
    'block_id',
    'order',
])


class TaskSession(namedtuple('TaskSession', [
        'task_session_id', 'student_id', 'task_id',
        'solved', 'given_up',
        'start', 'end'])):
    __slots__ = ()

    def __new__(cls, task_session_id=None, student_id=None, task_id=None,
                     solved=False, given_up=False, start=None, end=None):
        return super().__new__(cls,
            task_session_id=task_session_id,
            student_id=student_id,
            task_id=task_id,
            solved=solved,
            given_up=given_up,
            start=start,
            end=end)

    @property
    def time_spent(self):
        delta = self.end - self.start
        rounded_time = delta - timedelta(microseconds=delta.microseconds)
        time = max(rounded_time, timedelta(seconds=1))
        return time


ProgramSnapshot = namedtuple('ProgramSnapshot', [
    'program_snapshot_id',
    'task_session_id',
    'order',
    'time',
    'program',
    'execution', # snapshots are taken when a program is executed (-> True) or edited (-> False)
    'correct',  # boolean for executions, None for edits
])


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
