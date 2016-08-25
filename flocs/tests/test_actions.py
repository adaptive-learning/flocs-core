from flocs.actions import Action, ActionType, ActionCreators


def test_create_student_with_id():
    action = ActionCreators.create_student(student_id=17)
    expected_action = Action(
        type=ActionType.create_student,
        data={'student_id': 17},
        context=None,
        meta=None,
    )
    assert action == expected_action


def test_create_student_without_id():
    context = {'randomness_seed': 1}
    action = ActionCreators.create_student(context=context)
    expected_action = Action(
        type=ActionType.create_student,
        data={'student_id': 272996653310673477252411125948039410165},
        context=context,
        meta=None,
    )
    assert action == expected_action
