"""Tasks generated from data/tasks/*.md
"""
from ..entities import Task

# pylint:disable=line-too-long
TASKS = (
    Task(task_id='ladder', setting={'fields': [[('b', []), ('b', ['A']), ('b', ['M']), ('b', ['A']), ('b', [])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', ['S']), ('k', ['A']), ('k', [])]]}, solution=[['while', ['color', '!=', 'b'], [['move', 'ahead+shot'], ['move', 'ahead']]]]),
    Task(task_id='diamond-on-right', setting={'fields': [[('b', []), ('b', ['M']), ('b', []), ('b', []), ('b', [])], [('k', []), ('k', []), ('k', []), ('k', ['A']), ('k', [])], [('k', ['A']), ('k', []), ('k', []), ('k', []), ('k', ['D'])], [('k', []), ('k', ['M']), ('k', []), ('k', []), ('k', [])], [('k', []), ('k', []), ('k', ['S']), ('k', []), ('k', ['M'])]]}, solution=[['move', 'right'], ['move', 'right'], ['move', 'ahead'], ['move', 'ahead']]),
    Task(task_id='one-step-forward', setting={'fields': [[('b', []), ('b', []), ('b', [])], [('k', []), ('k', ['S']), ('k', [])]]}, solution=[['move', 'ahead']]),
    Task(task_id='turning-left', setting={'fields': [[('b', ['M']), ('b', []), ('b', []), ('b', ['M']), ('b', [])], [('k', ['A']), ('k', []), ('k', ['M']), ('k', []), ('k', ['A'])], [('k', []), ('k', []), ('k', ['A']), ('k', ['M']), ('k', [])], [('k', ['M']), ('k', []), ('k', ['S']), ('k', []), ('k', ['A'])]]}, solution=[['move', 'left'], ['move', 'ahead'], ['move', 'ahead']]),
    Task(task_id='shooting', setting={'fields': [[('b', ['A']), ('b', ['A']), ('b', ['A']), ('b', []), ('b', ['A'])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A'])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A'])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', []), ('k', ['A'])], [('k', ['A']), ('k', []), ('k', []), ('k', []), ('k', ['A'])], [('k', ['A']), ('k', []), ('k', ['S']), ('k', []), ('k', ['A'])]]}, solution=[['move', 'right'], ['move', 'ahead+shot'], ['move', 'ahead+shot'], ['move', 'ahead'], ['move', 'ahead']]),
    Task(task_id='yellow-condition', setting={'fields': [[('b', []), ('b', []), ('b', []), ('b', []), ('b', [])], [('k', []), ('k', []), ('k', []), ('k', []), ('k', [])], [('k', []), ('k', []), ('y', []), ('k', []), ('k', [])], [('k', []), ('k', []), ('k', ['S']), ('k', []), ('k', [])]]}, solution=[['move', 'ahead'], ['if', ['color', '==', 'y'], [['move', 'ahead']]]]),
    Task(task_id='turning-right-and-left', setting={'fields': [[('b', []), ('b', ['M']), ('b', []), ('b', ['M']), ('b', ['A'])], [('k', []), ('k', ['A']), ('k', ['A']), ('k', []), ('k', ['M'])], [('k', ['A']), ('k', ['M']), ('k', []), ('k', ['M']), ('k', ['A'])], [('k', ['M']), ('k', []), ('k', ['S']), ('k', ['M']), ('k', [])]]}, solution=[['move', 'ahead'], ['move', 'right'], ['move', 'left']]),
    Task(task_id='three-steps-forward', setting={'fields': [[('b', []), ('b', []), ('b', []), ('b', []), ('b', [])], [('k', []), ('k', []), ('k', []), ('k', []), ('k', [])], [('k', []), ('k', []), ('k', []), ('k', []), ('k', [])], [('k', []), ('k', []), ('k', ['S']), ('k', []), ('k', [])]]}, solution=[['move', 'ahead'], ['move', 'ahead'], ['move', 'ahead']]),
    Task(task_id='turning-left-and-right', setting={'fields': [[('b', []), ('b', ['M']), ('b', []), ('b', ['M']), ('b', [])], [('k', ['M']), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A'])], [('k', []), ('k', ['M']), ('k', ['S']), ('k', []), ('k', ['M'])]]}, solution=[['move', 'left'], ['move', 'right'], ['move', 'ahead']]),
    Task(task_id='zig-zag', setting={'fields': [[('b', []), ('b', []), ('b', []), ('b', []), ('b', [])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', []), ('k', ['A'])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', []), ('k', ['A'])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', []), ('k', ['A'])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', ['A']), ('k', []), ('k', ['A']), ('k', []), ('k', ['A'])], [('k', []), ('k', []), ('k', ['S']), ('k', []), ('k', [])]]}, solution=[['while', ['color', '!=', 'b'], [['move', 'right'], ['move', 'left']]]]),
    Task(task_id='turning-right', setting={'fields': [[('b', []), ('b', ['M']), ('b', []), ('b', []), ('b', ['M'])], [('k', ['A']), ('k', []), ('k', ['M']), ('k', []), ('k', ['A'])], [('k', []), ('k', ['M']), ('k', ['A']), ('k', []), ('k', [])], [('k', ['A']), ('k', []), ('k', ['S']), ('k', []), ('k', ['M'])]]}, solution=[['move', 'right'], ['move', 'ahead'], ['move', 'ahead']]),
    Task(task_id='shot', setting={'fields': [[('b', []), ('b', ['A']), ('b', []), ('b', ['A']), ('b', [])], [('k', []), ('k', ['A']), ('k', ['M']), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', []), ('k', ['A']), ('k', [])], [('k', []), ('k', ['A']), ('k', ['S']), ('k', ['A']), ('k', [])]]}, solution=[['move', 'ahead+shot'], ['move', 'ahead'], ['move', 'ahead']]),
)