from persiantools import utils


def ar_to_fa(string: str) -> str:
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

    return utils.replace(string, characters_map)


def fa_to_ar(string: str) -> str:
    """Convert Persian characters to Arabic

    Usage::
        from persiantools import characters
        converted = characters.ar_to_fa("ای چرخ فلک خرابی از کینه تست")

    :param string: A string, will be converted
    :rtype: str
    """
    characters_map = {"ی": "ي", "ک": "ك"}

    return utils.replace(string, characters_map)
