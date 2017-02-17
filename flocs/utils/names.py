""" Conversion between various naming conventions
"""
from functools import singledispatch
import re

@singledispatch
def camel_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake_case_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return snake_case_name

@camel_to_snake_case.register(dict)
def _camel_to_snake_case(mapping):
    return {camel_to_snake_case(key): value for key, value in mapping.items()}
