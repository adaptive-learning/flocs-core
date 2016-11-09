"""Unit tests of recommendation strategies
"""
from flocs.recommendation import recommend_task, Criterion
from flocs.tests.fixtures_entities import ENTITIES, tasks_dict


def test_recommend_single_task():
    ANY_TASK = 'task1'
    task = recommend_task(None, [ANY_TASK], criteria=[])
    assert task == ANY_TASK


def test_recommend_task():
    def stupid_score_function1(student, task):
        return student.student_id + task
    def stupid_score_function2(student, task):
        del student  # intentionally unused argument
        return 10000 / task
    crit1 = Criterion(weight=0.3, func=stupid_score_function1)
    crit2 = Criterion(weight=0.7, func=stupid_score_function2)
    student = ENTITIES['stud2']
    tasks = tasks_dict('t2', 't3')
    recommended_task = recommend_task(student=student, tasks=tasks, criteria=[crit1, crit2])
    expected_task = ENTITIES['t3'].task_id
    assert recommended_task == expected_task
