"""Converting tasks sources (in Markdown) into a Python module
"""

SOURCES_DIR = 'data/tasks/'
DEST = 'flocs/data/tasks.py'
#SOURCE_CONTENT_SPEC = {
#    'Setting': parse_setting,
#    'Solution': parse_solution,
#}


def main(dry=False):
    """Converts tasks sources into a a Python module

    Args:
        dry: if True, do not overwrite Python module, just print it
    """
    pass


def parse_task_source(file_name, file_content):
    pass


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

    PROGRAM -> SEQ
    SEQ -> CMD | CMD \n SEQ
    CMD -> MOVE | WHILE | REPEAT | (...)
    MOVE -> move() | move('ahead') | move('left') | move('right')
    WHILE -> while COND: \n{ SEQ }  # { and } denotes indentation change
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
    [['move'], ['while', ['color()', '!=', 'b'], [['move', 'right'],  ['move', 'left']]]]
    """
    # TODO: implement; (fake result for now)
    return ['move', ['move', 'right']]


if __name__ == "__main__":
    main()
