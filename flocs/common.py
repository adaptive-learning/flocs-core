""" Pure functions extracting information from the world state
"""
from datetime import timedelta
from uuid import uuid4


def new_id(state):
    if state.context.new_id == 'uuid':
        return uuid4()
    if state.context.new_id == 'seq':
        return state.total_entities()
    return state.context.new_id


def get_current_session_id(state, student_id, new_if_none=True):
    session = state.sessions.filter(student_id=student_id).order_by('end').last()
    if not session or session_too_old(session, state.context.time):
        return new_id(state) if new_if_none else None
    return session.session_id


def session_too_old(session, time):
    time_passed = time - session.end
    too_old = time_passed >= timedelta(hours=5)
    return too_old





def get_next_snapshot_order(state, task_session_id):
    snapshots = state.program_snapshots.filter(task_session_id=task_session_id)
    return len(snapshots) + 1
