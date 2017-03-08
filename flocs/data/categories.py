""" All available categories
"""
from ..entities import Category

# pylint:disable=line-too-long
# pylint:disable=bad-whitespace
categories = (
    Category(category_id='moves',           level_id=1, toolbox_id='fly'),
    Category(category_id='world',           level_id=2, toolbox_id='shoot'),
    Category(category_id='repeat',          level_id=3, toolbox_id='repeat'),
    Category(category_id='while',           level_id=4, toolbox_id='while'),
    Category(category_id='loops',           level_id=5, toolbox_id='loops'),
    Category(category_id='if',              level_id=6, toolbox_id='loops+if'),
    Category(category_id='comparing',       level_id=7, toolbox_id='loops+if+position'),
    Category(category_id='if-else',         level_id=8, toolbox_id='loops+if+else'),
    Category(category_id='final-challenge', level_id=9, toolbox_id='complete'),
    Category(category_id='uncategorized',   level_id=9, toolbox_id='complete'),
)
