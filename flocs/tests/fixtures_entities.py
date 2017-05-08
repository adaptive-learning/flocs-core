""" Common entities for testing purposes
"""
from flocs.entities import Task, Student, Category, Level, TaskSession

s1 = Student(student_id=1, credits=0)
s2 = Student(student_id=2, credits=2)

t1 = Task(task_id=1, category_id=None, setting=None, solution=None)
t2 = Task(task_id=2, category_id=1, setting=None, solution=None)
t3 = Task(task_id=3, category_id=None, setting=None, solution=None)
t4 = Task(task_id=4, category_id=None, setting=None, solution=None)
t5 = Task(task_id=5, category_id=2, setting=None, solution=None)
t6 = Task(task_id=6, category_id=None, setting=None, solution=None)
t7 = Task(task_id=7, category_id=None, setting=None, solution=None)
t8 = Task(task_id=8, category_id=None, setting=None, solution=None)
t9 = Task(task_id=9, category_id=3, setting=None, solution=None)

ts1 = TaskSession(task_session_id=1, student_id=1, task_id=2, solved=True, given_up=False, start=None, end=None)

c1 = Category(category_id=1, level_id=1, toolbox_id=None)
c2 = Category(category_id=2, level_id=2, toolbox_id=None)
c3 = Category(category_id=3, level_id=3, toolbox_id=None)

l1 = Level(level_id=1, credits=1)
l2 = Level(level_id=2, credits=2)
l3 = Level(level_id=3, credits=3)
