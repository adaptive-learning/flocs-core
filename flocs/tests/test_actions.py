from flocs import actions
from flocs.actions import Action
from flocs.state import State
from flocs.meta import META


def test_create_student():
    action = actions.create_student(student_id=17)
    expected_action = Action(
        type='create_student',
        data={'student_id': 17},
        context=None,
        meta=META,
    )
    assert action == expected_action


def test_create_student_at_state():
    state = State(entities='E', context='C', meta='M')
    action = actions.create_student(student_id=17).at(state)
    expected_action = Action(
        type='create_student',
        data={'student_id': 17},
        context='C',
        meta=META,
    )
    assert action == expected_action


def test_create_student_without_id(monkeypatch):
    monkeypatch.setattr('flocs.context.uuid4', lambda: 974375)
    action = actions.create_student()
    expected_action = Action(
        type='create_student',
        data={'student_id': 974375},
        context=None,
        meta=META,
    )
    assert action == expected_action
