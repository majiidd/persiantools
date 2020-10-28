# -*- coding: utf-8 -*-
import re

try:
    basestring
except NameError:
    basestring = str


def replace(string, dictionary):
    if not isinstance(string, basestring):
        raise TypeError("accept string type")

    pattern = re.compile("|".join(dictionary.keys()))
    return pattern.sub(lambda x: dictionary[x.group()], string)
