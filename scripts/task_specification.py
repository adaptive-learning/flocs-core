"""Task format specification
"""
import re
from flocs.entities import Task
from . import js_services


def parse_task(file_name, file_content):
    """
    >>> content = '''
    ... Setting
    ... -------
    ...
    ... ```
    ... |b |b |bR|
    ... |k |kS|k |
    ... ```
    ...
    ... Solution
    ... --------
    ...
    ... ```python
    ... move('ahead')
    ... ```
    ... '''
    >>> parse_task('one-step-forward', content)
    Task(task_id='one-step-forward', setting={'fields': [[('b', []), ...], ...]}, solution=[['move', 'ahead']])
    """
    SECTIONS_RE = re.compile(r"""
        \n* Setting
        \n  -------
        \n+ ```
            (?P<fields>.*?)
            ```
        \n
        \n* Solution
        \n  --------
        \n+ ```python
            (?P<solution>.*?)
            ```
        \n*
        """, re.VERBOSE | re.DOTALL)
    match = SECTIONS_RE.fullmatch(file_content)
    if not match:
        raise ValueError('Incorrect basic task source structure, '
                         'see task_specifiaction.SECTIONS_RE.')
    task_id = compute_task_id(file_name)
    fields = parse_fields(match.group('fields'))
    solution = parse_solution(match.group('solution'))
    task = Task(task_id=task_id, setting={'fields': fields}, solution=solution)
    return task


def compute_task_id(file_name):
    """Task_id is currently simply the file name (may change in future)
    """
    # hex(abs(hash(file_name)))[2:]
    # uuid.uuid5(uuid.NAMESPACE_DNS, file_name)
    return file_name


def parse_fields(text):
    """
    >>> text = '''
    ... |b |b |bR|
    ... |k |kS|k |
    ... '''
    >>> parse_fields(text)
    [[('b', []), ('b', []), ('b', ['R'])], [('k', []), ('k', ['S']), ('k', [])]]
    """
    AVAILABLE_COLORS = {
        'b': 'blue',
        'k': 'black',
        'g': 'grey',
        'y': 'yellow',
    }
    AVAILABLE_OBJECTS = {
        'S': 'spaceship',
        'A': 'asteroid',
        'M': 'meteoroid',
        'D': 'diamond',
    }
    # TODO: parse structure (2D maze, color+objects, apply additional tests
    #       - each color is among AVAILABLE_COLORS
    #       - each object is among AVAILABLE_OBJECTS
    #       - exactly 1 spaceship; at the bottom
    #       - final blue line and no blue color elsewhere
    lines = text.strip().split('\n')
    fields = [[parse_token(token)
                for token in line.strip().split('|') if token != '']
               for line in lines]
    return fields


def parse_token(string):
    """
    >>> parse_token('b ')
    ('b', [])
    >>> parse_token('bR')
    ('b', ['R'])
    >>> parse_token('bRRS')
    ('b', ['R', 'R', 'S'])
    """
    if not string or string[0] == ' ':
        raise ValueError(
            'Incorrect field token |{token}| - missing color (first character)'
            .format(token=string))
    color = string[0]
    objects = [char for char in string[1:] if char != ' ']
    return (color, objects)


def parse_solution(text):
    """Parse RoboCode text source into AST-tree (in plain JSON).

    >>> text = '''
    ... move()
    ... while color() != 'b':
    ...     move('right')
    ...     move('left')
    ... '''
    >>> parse_solution(text)
    [['move', 'ahead'], ['while', ['color', '!=', 'b'], [['move', 'right'], ['move', 'left']]]]
    """
    return js_services.parse_robocode(text)
