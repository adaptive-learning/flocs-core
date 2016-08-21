""" Actions represent intreactions and events in the world which we model

Future actions include:
    - ChangePackageVersion
    - StartSession
    - AttemptTask
    - ReportFlow
"""
from collections import namedtuple


CreateStudent = namedtuple('CreateStudent', [
    'student_id',
    'name',
])


StartTask = namedtuple('StartTask', [
    'task_instance_id',
    'student_id',
    'task_id',
])


SolveTask = namedtuple('SolveTask', [
    'task_instance_id',
])


GiveUpTask = namedtuple('GiveUpTask', [
    'task_instance_id',
])
