""" Actions represent events and interactions in the world we want to model
"""
from enum import Enum
from flocs.action_factory import ActionIntent
from flocs.extractors import new_id, get_current_session_id
from flocs.extractors import get_student_id_for_task_session
from flocs.extractors import get_task_id_for_task_session


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
        student_id = self.data['student_id']
        current_session_id = get_current_session_id(state, student_id, new_if_none=False)
        discarded = current_session_id is not None
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

    def discard_action(self, state):
        """ Don't start task if the task was already started in this session
        """
        student_id = self.data['student_id']
        task_id = self.data['task_id']
        session_id = get_current_session_id(state, student_id, new_if_none=False)
        if session_id is None:
            return False
        session = state.sessions[session_id]
        task_session = state.task_sessions \
            .filter(student_id=student_id, task_id=task_id).order_by('start').last()
        if not task_session:
            return False
        discarded = task_session.start >= session.start
        return discarded


class SolveTask(ActionIntent):
    """ Student has solved a task
    """
    required_fields = ['task_session_id']
    auto_fields = [
        ('student_id', get_student_id_for_task_session, 'task_session_id'),
        ('task_id', get_task_id_for_task_session, 'task_session_id'),
        ('session_id', get_current_session_id, 'student_id'),
    ]


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
