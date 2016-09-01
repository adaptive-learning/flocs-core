"""Context is a part of the world state changing continuously
"""
import random
import sys
from datetime import datetime
from uuid import uuid4


STATIC_CONTEXT = {
    'time': datetime(1, 1, 1),
    'randomness': 0,
}


def static_context_generator():
    while True:
        yield STATIC_CONTEXT


def default_context_generator():
    while True:
        context = {
            'time': datetime.now(),
            'randomness': random.randint(0, sys.maxsize),
        }
        yield context


def generate_id_if_not_set(maybe_id):
    just_id = maybe_id if maybe_id is not None else uuid4()
    return just_id
