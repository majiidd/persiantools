# -*- coding: utf-8 -*-
from persiantools import utils, PY2


def en_to_fa(string):
    """Convert EN digits to Persian

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.en_to_fa("0123456789")

        :param string:  A string, will be converted
        :rtype: str
    """
    digits_map = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    if PY2:
        if isinstance(string, unicode):
            digits_map = {unicode(e, "utf8"): unicode(f, "utf8") for e, f in digits_map.iteritems()}

    return utils.replace(string, digits_map)


def ar_to_fa(string):
    """Convert Arabic digits to Persian

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.ar_to_fa("٠١٢٣٤٥٦٧٨٩")

        :param string: A string, will be converted
        :rtype: str
        """
    digits_map = {
        "٠": "۰",
        "١": "۱",
        "٢": "۲",
        "٣": "۳",
        "٤": "۴",
        "٥": "۵",
        "٦": "۶",
        "٧": "۷",
        "٨": "۸",
        "٩": "۹",
    }

    if PY2:
        if isinstance(string, unicode):
            digits_map = {unicode(a, "utf8"): unicode(f, "utf8") for a, f in digits_map.iteritems()}

    return utils.replace(string, digits_map)


def fa_to_en(string):
    """Convert Persian digits to EN

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.fa_to_en("۰۱۲۳۴۵۶۷۸۹")

        :param string: A string, will be converted
        :rtype: str
        """
    digits_map = {
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
    }

    if PY2:
        if isinstance(string, unicode):
            digits_map = {unicode(f, "utf8"): unicode(e, "utf8") for f, e in digits_map.iteritems()}

    return utils.replace(string, digits_map)


def fa_to_ar(string):
    """Convert Persian digits to Arabic

        Usage::
        >>> from persiantools import digits
        >>> converted = digits.fa_to_ar("۰۱۲۳۴۵۶۷۸۹")

        :param string: A string, will be converted
        :rtype: str
        """
    digits_map = {
        "۰": "٠",
        "۱": "١",
        "۲": "٢",
        "۳": "٣",
        "۴": "٤",
        "۵": "٥",
        "۶": "٦",
        "۷": "٧",
        "۸": "٨",
        "۹": "٩",
    }

    if PY2:
        if isinstance(string, unicode):
            digits_map = {unicode(f, "utf8"): unicode(a, "utf8") for f, a in digits_map.iteritems()}

    return utils.replace(string, digits_map)
