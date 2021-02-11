from persiantools import utils


def en_to_fa(string: str) -> str:
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

    return utils.replace(string, digits_map)


def ar_to_fa(string: str) -> str:
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

    return utils.replace(string, digits_map)


def fa_to_en(string: str) -> str:
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

    return utils.replace(string, digits_map)


def fa_to_ar(string: str) -> str:
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

    return utils.replace(string, digits_map)
