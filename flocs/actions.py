""" Actions represent events and interactions in the world we want to model
"""
from enum import Enum
from flocs.base_action import BaseAction
from flocs.context import dynamic


def create(type='nothing-happens', data=None, context=dynamic):
    """ Create a new action of given type, with given data, in given context

    Args:
        type: one of flocs.actions.ActionTypes
        data: dictionary of data for given action type (using kebab-case keys)
        context: factory for getting time, randomness, version and new IDs

    Return:
        flocs.entities.Action
    """
    action_type = ActionType(type)
    action = action_type.creator.from_data(data, context)
    return action


class NothingHappens(BaseAction):
    """ Nothing particular happened (but time has passed)
    """
    auto_fields = []
    required_fields = []


class CreateStudent(BaseAction):
    """ New student appears in the system
    """
    auto_fields = ['student_id']
    required_fields = []


class StartTask(BaseAction):
    """ Student starts working on a task
    """
    auto_fields = ['task_session_id']
    required_fields = ['student_id', 'task_id']


class SolveTask(BaseAction):
    """ Student has solved a task
    """
    auto_fields = []
    required_fields = ['task_session_id']


class GiveUpTask(BaseAction):
    """ Student has given up a task
    """
    auto_fields = []
    required_fields = ['task_session_id']


class SeeInstruction(BaseAction):
    """ Student has seen an instruction
    """
    auto_fields = ['seen_instruction_id']
    required_fields = ['student_id', 'instruction_id']


class ActionType(str, Enum):
    """ Available action types and associated action creators
    """
    nothing_happens = 'nothing-happens'
    create_student = 'create-student'
    start_task = 'start-task'
    solve_task = 'solve-task'
    give_up_task = 'give-up-task'
    see_instruction = 'see-instruction'

    @property
    def creator(self):
        return {
            'nothing-happens': NothingHappens,
            'create-student': CreateStudent,
            'start-task': StartTask,
            'solve-task': SolveTask,
            'give-up-task': GiveUpTask,
            'see-instruction': SeeInstruction,
        }[self.value]


empty = create(type='nothing-happens', data={})
