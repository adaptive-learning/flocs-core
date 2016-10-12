"""Task format specification
"""
import re
from flocs.entities import Task


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
    Task(task_id='one-step-forward', setting=[[('b', []), ...], ...], solution=[['move', 'ahead']])
    """
    SECTIONS_RE = re.compile(r"""
        \n* Setting
        \n  -------
        \n+ ```
            (?P<setting>.*?)
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
    setting = parse_setting(match.group('setting'))
    solution = parse_solution(match.group('solution'))
    task = Task(task_id=task_id, setting=setting, solution=solution)
    return task


def compute_task_id(file_name):
    """Task_id is currently simply the file name (may change in future)
    """
    # hex(abs(hash(file_name)))[2:]
    # uuid.uuid5(uuid.NAMESPACE_DNS, file_name)
    return file_name


def parse_setting(text):
    """
    >>> text = '''
    ... |b |b |bR|
    ... |k |kS|k |
    ... '''
    >>> parse_setting(text)
    [[('b', []), ('b', []), ('b', ['R'])], [('k', []), ('k', ['S']), ('k', [])]]
    """
    AVAILABLE_COLORS = {
        'b': 'blue',
        'r': 'red',
        'y': 'yellow',
        'k': 'black',
    }
    AVAILABLE_OBJECTS = {
        'S': 'spaceship',
        'R': 'rock',
    }
    # TODO: parse structure (2D maze, color+objects, apply additional tests
    #       - each color is among AVAILABLE_COLORS
    #       - each object is among AVAILABLE_OBJECTS
    #       - exactly 1 spaceship; at the bottom
    #       - final blue line and no blue color elsewhere
    lines = text.strip().split('\n')
    setting = [[parse_token(token)
                for token in line.strip().split('|') if token != '']
               for line in lines]
    return setting


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
    """Parse text of solution in Python into a JSON representation according to
    the following grammar (NOTE: grammar should be specified in code, not in
    a comment, otherwise it gets out of sync soon.

    TODO:
    Specification of RoboCode programming language.
    This language is used by students to solve tasks in RoboGame.
    -> but implement the parser in JS (we will need it in fr-app as well)

    PROGRAM -> SEQ
    SEQ -> CMD | CMD \n SEQ
    CMD -> MOVE | WHILE | REPEAT | (...)
    MOVE -> move() | move('ahead') | move('left') | move('right')
    WHILE -> while COND: \n{ SEQ }  # { and } denotes indentation change
    REPEAT -> repeat COND: \n{ SEQ }
    COND -> COND and COND | COND or COND | VAL REL VAL
    VAL -> COLOR | NUM
    COLOR -> color() | 'b' | 'r' | 'y' | 'k'
    NUM -> pos() | 1 | 2 | 3 | 4 | 5
    REL -> == | != | > | >= | < | <=
    >>> text = '''
    ... move()
    ... while color() != 'b':
    ...     move('right')
    ...     move('left')
    ... '''
    >>> parse_solution(text)
    [['move', 'ahead'], ['while', ['color', '!=', 'b'], [['move', 'right'],  ['move', 'left']]]]
    """
    # TODO: implement; (fake result for now)
    return [['move', 'ahead']]


