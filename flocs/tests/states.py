"""
Some worldstates for testing purposes
"""
from datetime import datetime
from flocs.entities import Student, TaskInstance
from flocs.state import State, LazyValue

# ---------------------------------------------------------------------------

STATE_0 = State()

# ---------------------------------------------------------------------------

STATE_1 = State({
    'entities.students': {
        0: Student(student_id=0),
        },
    })

# ---------------------------------------------------------------------------

STATE_2 = State({
    'entities.students': {
        0: Student(student_id=0),
        1: Student(student_id=1),
        },
    })

# ---------------------------------------------------------------------------

STATE_3 = State({
    'entities.students': {
        0: Student(student_id=0),
        1: Student(student_id=1),
        },
    'entities.task_instances': {
        0: TaskInstance(
            task_instance_id=0,
            task_id=0,
            student_id=0,
            solved=False,
            given_up=False,
        ),
        }
    })

# ---------------------------------------------------------------------------

STATE_4 = State({
    'entities.students': {
        0: Student(student_id=0),
        1: Student(student_id=1),
        },
    'entities.task_instances': {
        0: TaskInstance(
            task_instance_id=0,
            task_id=0,
            student_id=0,
            solved=True,
            given_up=False,
        ),
        }
    })

# ---------------------------------------------------------------------------

LAZY_STATE_1 = State({
    'entities.students': LazyValue(lambda: {
        0: Student(student_id=0),
        1: Student(student_id=1),
        }),
    'entities.task_instances': LazyValue(lambda: {
        0: TaskInstance(
            task_instance_id=0,
            task_id=0,
            student_id=0,
            solved=False,
            given_up=False,
        ),
        }),
    'context.time': datetime(2000, 1, 30),
    'context.randomness_seed': 4,
    })

# ---------------------------------------------------------------------------
