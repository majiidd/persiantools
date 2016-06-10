# -*- coding: utf-8 -*-
import re


def replace(string, dictionary):
    if not isinstance(string, str):
        raise ValueError("accept string type")

    pattern = re.compile('|'.join(dictionary.keys()))
    return pattern.sub(lambda x: dictionary[x.group()], string)


def check_int_field(value):
    if isinstance(value, int):
        return value

    if not isinstance(value, float):
        try:
            value = value.__int__()
        except AttributeError:
            pass
        else:
            if isinstance(value, int):
                return value

            raise TypeError('__int__ returned non-int (type %s)' % type(value).__name__)

        raise TypeError('an integer is required (got type %s)' % type(value).__name__)

    raise TypeError('integer argument expected, got float')
