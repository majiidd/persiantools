# -*- coding: utf-8 -*-
import re


def replace(string, dictionary):
    if not isinstance(string, str):
        raise ValueError("accept string type")

    pattern = re.compile('|'.join(dictionary.keys()))
    return pattern.sub(lambda x: dictionary[x.group()], string)
