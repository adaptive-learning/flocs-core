"""
Some worldstates for testing purposes
"""
from collections import ChainMap
#from datetime import datetime
from flocs.entities import Student, TaskInstance
from flocs.state import create_state, STATIC_ENTITIES, STATIC_CONTEXT

# ---------------------------------------------------------------------------

STATE_0 = create_state(
    entities=STATIC_ENTITIES,
    context=STATIC_CONTEXT,
)

# ---------------------------------------------------------------------------

STATE_1 = create_state(
    entities=ChainMap({
        Student: {
            0: Student(student_id=0),
        }},
        STATIC_ENTITIES,
    ),
    context=STATIC_CONTEXT,
)

# ---------------------------------------------------------------------------

STATE_2 = create_state(
    entities=ChainMap({
        Student: {
            0: Student(student_id=0),
            1: Student(student_id=1),
        }},
        STATIC_ENTITIES,
    ),
    context=STATIC_CONTEXT,
)

# ---------------------------------------------------------------------------

STATE_3 = create_state(
    entities=ChainMap({
        Student: {
            0: Student(student_id=0),
            1: Student(student_id=1),
        },
        TaskInstance: {
            0: TaskInstance(
                task_instance_id=0,
                task_id=0,
                student_id=0,
                solved=False,
                given_up=False,
            ),
        }},
        STATIC_ENTITIES,
    ),
    context=STATIC_CONTEXT,
)

# ---------------------------------------------------------------------------

STATE_4 = create_state(
    entities=ChainMap({
        Student: {
            0: Student(student_id=0),
            1: Student(student_id=1),
        },
        TaskInstance: {
            0: TaskInstance(
                task_instance_id=0,
                task_id=0,
                student_id=0,
                solved=True,
                given_up=False,
            ),
        }},
        STATIC_ENTITIES,
    ),
    context=STATIC_CONTEXT,
)
