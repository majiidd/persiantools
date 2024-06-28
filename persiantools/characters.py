from persiantools import utils


def ar_to_fa(string: str) -> str:
    """
    Convert Arabic characters to Persian.

    Usage::
        from persiantools import characters
        converted = characters.ar_to_fa("السلام عليكم")

    Args:
    string (str): The string to convert.

    Returns:
    str: The converted string with Arabic characters replaced by Persian characters.

    Raises:
    TypeError: If the input string is not of type str.
    """
    if not isinstance(string, str):
        raise TypeError("Input must be of type str")

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
    """
    Convert Persian characters to Arabic.

    Usage::
        from persiantools import characters
        converted = characters.fa_to_ar("ای چرخ فلک خرابی از کینه تست")

    Args:
    string (str): The string to convert.

    Returns:
    str: The converted string with Persian characters replaced by Arabic characters.

    Raises:
    TypeError: If the input string is not of type str.
    """
    if not isinstance(string, str):
        raise TypeError("Input must be of type str")

    characters_map = {"ی": "ي", "ک": "ك"}

    return utils.replace(string, characters_map)
