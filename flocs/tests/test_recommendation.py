from flocs.recommendation import recommend_task


def test_recommend_single_task():
    ANY_TASK = 'task1'
    task = recommend_task(None, [ANY_TASK], criteria=[])
    assert task == ANY_TASK
