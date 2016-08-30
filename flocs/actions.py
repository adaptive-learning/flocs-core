"""Actions represent events and interactions in the world we want to model

Future actions include:
    - ChangePackageVersion
    - StartSession
    - AttemptTask
    - ReportFlow
"""
from collections import namedtuple
from flocs import __version__ as package_version
from flocs.context import generate_id_if_not_set


Action = namedtuple('Action', [
    'type',     # one of the string from the finite set of actions (ActionType enum)
    'data',     # dictionary of data specific to this action
    'context',  # optionally specified context (part of the state changing continuously, e.g. time)
    'meta',     # optionally specified mata-information, such as package version
])


def action_creator(action_data_creator):
    """Decorate function to make it an action creator
    >>> @action_creator
    ... def create_fruit(name, fruit_id=None):
    ...     fruit_id = fruit_id if fruit_id is not None else 8
    ...     return {'fruit_id': fruit_id, 'name': name}
    >>> action = create_fruit(name='kiwi')
    >>> action
    Action(type='create_fruit', data={...}, context={...}, meta={...})
    >>> import pprint  # to make the output deterministic (sorted keys)
    >>> pprint.pprint(action.data)
    {'fruit_id': 8, 'name': 'kiwi'}
    """
    action_type = action_data_creator.__name__
    def wrapped_action_creator(*args, context=None, **kwargs):
        # TODO: should probably also pass requested context attributes
        data = action_data_creator(*args, **kwargs)
        context = context or {}
        meta = create_action_meta()
        return Action(type=action_type, data=data, context=context, meta=meta)
    return wrapped_action_creator


def create_action_meta():
    meta = {
        'version': package_version,
    }
    return meta


@action_creator
def create_student(student_id=None):
    """A new student exists in the world

    >>> create_student(student_id=16)
    Action(type='create_student', data={'student_id': 16}, context=None, meta=None)
    """
    return {
        'student_id': generate_id_if_not_set(student_id),
    }


@action_creator
def start_task(student_id, task_id, task_instance_id=None):
    """A student starts working on a task

    >>> start_task(student_id=16, task_id=4, task_instance_id=8)
    Action(type='start_task', data={'student_id': 16, 'task_id': 4, 'task_instance_id': 1}, context=None, meta=None)
    """
    return {
        'task_instance_id': generate_id_if_not_set(task_instance_id),
        'student_id': student_id,
        'task_id': task_id,
    }


@action_creator
def solve_task(task_instance_id):
    """A student has solve a task

    >>> solve_task(task_instance_id=8)
    Action(type='solve_task', data={'task_instance_id': 8}, context=None, meta=None)
    """
    return {
        'task_instance_id': task_instance_id,
    }


@action_creator
def give_up_task(task_instance_id):
    """A student has given up a task

    >>> give_up_task(task_instance_id=8)
    Action(type='give_up_task', data={'task_instance_id': 8}, context=None, meta=None)
    """
    return {
        'task_instance_id': task_instance_id,
    }
