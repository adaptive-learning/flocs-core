"""Unit tests for context
"""

from flocs import context
from datetime import datetime
from random import randint


def test_static_context_generator():
    expected = context.STATIC_CONTEXT
    zeroth = next(context.static_context_generator())
    rand = randint(10, 20)
    for _ in range(rand):
        randomth = next(context.static_context_generator())
    assert zeroth == randomth == expected


def test_default_context_generator(monkeypatch):
    monkeypatch.setattr('flocs.context.random.randint',
                        lambda x, y: 516)
    expected = {'time': datetime(2016, 11, 9, 11, 1, 28, 277932),
                'randomness': 516}
    zeroth = next(context.default_context_generator())
    rand = randint(10, 20)
    for _ in range(rand):
        randomth = next(context.default_context_generator())
    assert type(zeroth['time']) == type(randomth['time']) == type(expected['time'])
    assert zeroth['randomness'] == randomth['randomness'] == expected['randomness']


def test_generate_id_if_not_set_is_set():
    expected = 55
    generated = context.generate_id_if_not_set(55)
    assert expected == generated


def test_generate_id_if_not_set_is_not_set(monkeypatch):
    monkeypatch.setattr('flocs.context.uuid4', lambda: 974)
    expected = 974
    generated = context.generate_id_if_not_set(None)
    assert expected == generated
