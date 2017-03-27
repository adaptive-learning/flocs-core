""" Common world-states for testing purposes
"""
from flocs.state import empty
from flocs.context import static
from .fixtures_entities import s1, t1, t2, t3, t4, t5

w0 = empty + static
w1 = w0 + s1 + t1 + t2 + t3 + t4 + t5
