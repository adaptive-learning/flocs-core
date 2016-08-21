""" Intents to perform some action

Intents performers are function accepting information known before an action
was taken  (e.g. not an ID of created object or time of the action) and return
an action.
"""

def create_student(store):
    raise NotImplementedError


def create_task_instance(store, student_id, task_id):
    raise NotImplementedError


def update_task_instance(store, task_instance):
    raise NotImplementedError
