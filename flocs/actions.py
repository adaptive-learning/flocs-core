""" Actions represent events and interactions in the world we want to model
"""
from datetime import timedelta
from enum import Enum
from flocs.action_factory import ActionIntent
from flocs.extractors import new_id, get_current_session_id


def create(type='nothing-happens', data=None):
    """ Create a new action of given type and with given data

    Args:
        type: one of flocs.actions.ActionTypes
        data: dictionary of data for given action type (using kebab-case keys)

    Return:
        flocs.entities.Action
    """
    action_type = ActionType(type)
    data_dict = data or {}
    action = action_type.creator(**data_dict)
    return action


class NothingHappens(ActionIntent):
    """ Nothing particular happened (but time has passed)
    """
    auto_fields = []
    required_fields = []


class StartSession(ActionIntent):
    """ Student starts interacting with the learning system
    """
    required_fields = []
    auto_fields = [
        ('session_id', new_id),
        ('student_id', new_id),
    ]

    def discard_action(self, state):
        last_session_id = get_current_session_id(state, self.data['student_id'])
        if not last_session_id:
            return False
        last_time = state.sessions[last_session_id].end_time
        interval = state.context.time - last_time
        discarded = interval < timedelta(hours=5)
        return discarded


class StartTask(ActionIntent):
    """ Student starts working on a task
    """
    required_fields = [
        'student_id',
        'task_id',
    ]
    auto_fields = [
        ('task_session_id', new_id),
        ('session_id', get_current_session_id, 'student_id'),
    ]


class SolveTask(ActionIntent):
    """ Student has solved a task
    """
    required_fields = ['task_session_id']
    auto_fields = []


class GiveUpTask(ActionIntent):
    """ Student has given up a task
    """
    required_fields = ['task_session_id']
    auto_fields = []


class SeeInstruction(ActionIntent):
    """ Student has seen an instruction
    """
    required_fields = ['student_id', 'instruction_id']
    auto_fields = [
        ('seen_instruction_id', new_id)
    ]


class ActionType(str, Enum):
    """ Available action types and associated action creators
    """
    nothing_happens = 'nothing-happens'
    start_session = 'start-session'
    start_task = 'start-task'
    solve_task = 'solve-task'
    give_up_task = 'give-up-task'
    see_instruction = 'see-instruction'

    @property
    def creator(self):
        return {
            'nothing-happens': NothingHappens,
            'start-session': StartSession,
            'start-task': StartTask,
            'solve-task': SolveTask,
            'give-up-task': GiveUpTask,
            'see-instruction': SeeInstruction,
        }[self.value]


empty = create(type='nothing-happens', data={})
