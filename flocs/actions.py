"""Actions represent events and interactions in the world we want to model

Future actions include:
    - StartSession
    - AttemptTask
    - ReportFlow
"""
from enum import Enum
from flocs.context import dynamic, generate_id_if_not_set
from flocs import entities


class ActionType(str, Enum):
    """ Namespace for available action types
    """
    nothing_happens = 'nothing-happens'
    create_student = 'create-student'
    start_task = 'start-task'
    solve_task = 'solve-task'
    give_up_task = 'give-up-task'
    see_instruction = 'see-instruction'


def create(type=ActionType.nothing_happens, data=None, context=dynamic):
    """ Create a new action

    Usually, you will only want to pass type and data, but you can also
    provide action_id and factories for time and randomness.
    """
    # TODO: check that type is valid
    # TODO: enforce fixed actions structure (see CreateStudent below)
    action = entities.Action(
        action_id=context.new_id(),
        type=type,
        data=add_auto_fields(type, data, generate_id=context.new_id),
        time=context.time,
        randomness=context.randomness,
        version=context.version,
    )
    return action


def add_auto_fields(type, data, generate_id):
    enriched_data = {**data} if data else {}
    auto_fields = {
        ActionType.nothing_happens: (),
        ActionType.create_student: ('student_id',),
        ActionType.start_task: ('task_session_id',),
        ActionType.solve_task: (),
        ActionType.give_up_task: (),
        ActionType.see_instruction: ('seen_instruction_id',)
    }[type]
    for auto_field in auto_fields:
        enriched_data[auto_field] = generate_id()
    return enriched_data


# Consider more rigid and explicit structure of data fields, sth like:
#
# class CreateStudent(Action):
#     """A new student exists in the world
#     """
#     student_id = AutoField()


# Follows legacy code, TODO: refactor tests and flocs-web, so that these are not needed

def create_student(student_id=None):
    """A new student exists in the world
    """
    return create(
        type=ActionType.create_student,
        data={
            'student_id': generate_id_if_not_set(student_id),
        })


def start_task(student_id, task_id, task_session_id=None):
    """A student starts working on a task
    """
    return create(
        type=ActionType.start_task,
        data={
            'task_session_id': generate_id_if_not_set(task_session_id),
            'student_id': student_id,
            'task_id': task_id,
        })


def solve_task(task_session_id):
    """A student has solved a task
    """
    return create(
        type=ActionType.solve_task,
        data={
            'task_session_id': task_session_id,
        })


def give_up_task(task_session_id):
    """A student has given up a task
    """
    return create(
        type=ActionType.give_up_task,
        data={
            'task_session_id': task_session_id,
        })


def see_instruction(student_id, instruction_id, seen_instruction_id=None):
    """ Student has seen instruction
    """
    return create(
        type=ActionType.see_instruction,
        data={
            'seen_instruction_id': generate_id_if_not_set(seen_instruction_id),
            'student_id': student_id,
            'instruction_id': instruction_id,
        })


def nothing_happens():
    """ Nothing particular happened (but time has passed)
    """
    return create(
        type=ActionType.nothing_happens,
        data={})
