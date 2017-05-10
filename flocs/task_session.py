""" Pure functions extracting information related to task session from the world state
"""


def get_student_id(state, task_session_id):
    task_session = state.task_sessions[task_session_id]
    return task_session.student_id


def get_task_id(state, task_session_id):
    task_session = state.task_sessions[task_session_id]
    return task_session.task_id


def is_solved(state, student_id, task_id):
    solved_task_sessions = state.task_sessions.filter(student_id=student_id,
                                                      task_id=task_id,
                                                      solved=True)
    return solved_task_sessions.exists()


def get_time(state, student_id, task_id):
    """ Best time if student has solved the task, otherwise just the last time
    """
    task_sessions = state.task_sessions.filter(student_id=student_id, task_id=task_id)
    solved_task_sessions = task_sessions.filter(solved=True)
    if solved_task_sessions.exists():
        times = [ts.time_spent for ts in solved_task_sessions.values()]
        return min(times)
    last_task_session = task_sessions.order_by('end').last()
    return last_task_session.time_spent if last_task_session else None


def get_all_solved(state, student_id):
    return state.task_sessions.filter(student_id=student_id, solved=True)
