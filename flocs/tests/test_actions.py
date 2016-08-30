from flocs.actions import Action, create_student
from flocs import __version__


def test_create_student_with_id():
    action = create_student(student_id=17)
    expected_action = Action(
        type='create_student',
        data={'student_id': 17},
        context={},
        meta={'version': __version__},
    )
    assert action == expected_action



def test_create_student_without_id(monkeypatch):
    monkeypatch.setattr('flocs.context.uuid4', lambda: 974375)
    action = create_student()
    expected_action = Action(
        type='create_student',
        data={'student_id': 974375},
        context={},
        meta={'version': __version__},
    )
    assert action == expected_action
