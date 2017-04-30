""" Conversion between various naming conventions
"""
from functools import singledispatch
import re

@singledispatch
def camel_to_snake_case(name):
    partially_underscored = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    fully_underscored = re.sub('([a-z0-9])([A-Z])', r'\1_\2', partially_underscored)
    return fully_underscored.lower()


@camel_to_snake_case.register(dict)
def _camel_to_snake_case(mapping):
    return {camel_to_snake_case(key): value for key, value in mapping.items()}


@singledispatch
def camel_to_kebab_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    kebab_case_name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    return kebab_case_name


@singledispatch
def kebab_to_snake_case(name):
    return name.replace('-', '_')


@kebab_to_snake_case.register(dict)
def _kebab_to_snake_case(mapping):
    return {kebab_to_snake_case(key): value for key, value in mapping.items()}


def pluralize(name):
    if name[-1] in 'szx':
        return name + 'es'
    if name[-1] == 'y':
        return name[:-1] + 'ies'
    return name + 's'
