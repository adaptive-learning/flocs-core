""" Actions represent events and interactions in the world we want to model
"""
from enum import Enum
from flocs.action_factory import ActionIntent
from flocs.extractors import new_id, get_current_session_id
from flocs.extractors import get_student_id_for_task_session
from flocs.extractors import get_task_id_for_task_session
from flocs.extractors import get_next_snapshot_order


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

    def check_duplicate(self, state):
        """ Don't start session if another session is still active
        """
        student_id = self.data['student_id']
        current_session_id = get_current_session_id(state, student_id, new_if_none=False)
        if current_session_id is not None:
            self.raise_duplicate_action(session_id=current_session_id)


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

    def check_duplicate(self, state):
        """ Don't start task if it was already started in this session
        """
        student_id = self.data['student_id']
        task_id = self.data['task_id']
        session_id = get_current_session_id(state, student_id, new_if_none=False)
        if session_id is None:
            return
        session = state.sessions[session_id]
        task_session = state.task_sessions \
            .filter(student_id=student_id, task_id=task_id).order_by('start').last()
        if task_session and task_session.start >= session.start:
            self.raise_duplicate_action(task_session_id=task_session.task_session_id)


class EditProgram(ActionIntent):
    """ Student has made a change in their program
    """
    required_fields = (
        'task_session_id',
        'program',
    )
    auto_fields = (
        ('program_snapshot_id', new_id),
        ('student_id', get_student_id_for_task_session, 'task_session_id'),
        ('task_id', get_task_id_for_task_session, 'task_session_id'),
        ('session_id', get_current_session_id, 'student_id'),
        ('order', get_next_snapshot_order, 'task_session_id'),
    )


class RunProgram(ActionIntent):
    """ Student has executed their program
    """
    required_fields = (
        'task_session_id',
        'program',
        'correct',
    )
    auto_fields = (
        ('program_snapshot_id', new_id),
        ('student_id', get_student_id_for_task_session, 'task_session_id'),
        ('task_id', get_task_id_for_task_session, 'task_session_id'),
        ('session_id', get_current_session_id, 'student_id'),
        ('order', get_next_snapshot_order, 'task_session_id'),
    )


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
    run_program = 'run-program'
    edit_program = 'edit-program'
    solve_task = 'solve-task'
    give_up_task = 'give-up-task'
    see_instruction = 'see-instruction'

    @property
    def creator(self):
        return {
            'nothing-happens': NothingHappens,
            'start-session': StartSession,
            'start-task': StartTask,
            'run-program': RunProgram,
            'edit-program': EditProgram,
            'solve-task': SolveTask,
            'give-up-task': GiveUpTask,
            'see-instruction': SeeInstruction,
        }[self.value]


empty = create(type='nothing-happens', data={})
