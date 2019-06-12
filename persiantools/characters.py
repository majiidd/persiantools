# -*- coding: utf-8 -*-
from persiantools import utils, PY2


def ar_to_fa(string):
    """Convert Arabic characters to Persian

        Usage::
            from persiantools import characters
            converted = characters.ar_to_fa("السلام عليكم")

        :param string: A string, will be converted
        :rtype: str
        """
    characters_map = {
        "دِ": "د",
        "بِ": "ب",
        "زِ": "ز",
        "ذِ": "ذ",
        "شِ": "ش",
        "سِ": "س",
        "ى": "ی",
        "ي": "ی",
        "ك": "ک",
    }

    if PY2:
        if isinstance(string, unicode):
            characters_map = {
                unicode(a, "utf8"): unicode(f, "utf8") for a, f in characters_map.iteritems()
            }

    return utils.replace(string, characters_map)


def fa_to_ar(string):
    """Convert Persian characters to Arabic

        Usage::
            from persiantools import characters
            converted = characters.ar_to_fa("ای چرخ فلک خرابی از کینه تست")

        :param string: A string, will be converted
        :rtype: str
        """
    characters_map = {"ی": "ي", "ک": "ك"}

    if PY2:
        if isinstance(string, unicode):
            characters_map = {
                unicode(f, "utf8"): unicode(a, "utf8") for f, a in characters_map.iteritems()
            }

    return utils.replace(string, characters_map)
