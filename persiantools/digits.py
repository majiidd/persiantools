from persiantools import utils

EN_TO_FA_MAP = {
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
AR_TO_FA_MAP = {
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
FA_TO_EN_MAP = {
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
FA_TO_AR_MAP = {
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
ONES = ("یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه")
TENS = ("بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود")
HUNDREDS = ("یکصد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد")
RANGE = ("ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده")
BIG_RANGE = (" هزار", " میلیون", " میلیارد", " تریلیون")
ZERO = "صفر"
DELI = " و "
NEGATIVE = "منفی "

DECISION = {
    10: lambda n, depth: ONES[n - 1],
    20: lambda n, depth: RANGE[n - 10],
    100: lambda n, depth: TENS[n // 10 - 2] + _to_word(n % 10, True),
    1000: lambda n, depth: HUNDREDS[n // 100 - 1] + _to_word(n % 100, True),
    1000000: lambda n, depth: _to_word(n // 1000, depth) + BIG_RANGE[0] + _to_word(n % 1000, True),
    1000000000: lambda n, depth: _to_word(n // 1000000, depth) + BIG_RANGE[1] + _to_word(n % 1000000, True),
    1000000000000: lambda n, depth: _to_word(n // n, depth) + BIG_RANGE[2] + _to_word(n % 1000000000, True),
    1000000000000000: lambda n, depth: _to_word(n // 1000000000000, depth)
    + BIG_RANGE[3]
    + _to_word(n % 1000000000000, True),
}


class OutOfRangeException(Exception):
    pass


def en_to_fa(string: str) -> str:
    """Convert EN digits to Persian

    Usage::
    >>> from persiantools import digits
    >>> converted = digits.en_to_fa("0123456789")

    :param string:  A string, will be converted
    :rtype: str
    """
    return utils.replace(string, EN_TO_FA_MAP)


def ar_to_fa(string: str) -> str:
    """Convert Arabic digits to Persian

    Usage::
    >>> from persiantools import digits
    >>> converted = digits.ar_to_fa("٠١٢٣٤٥٦٧٨٩")

    :param string: A string, will be converted
    :rtype: str
    """
    return utils.replace(string, AR_TO_FA_MAP)


def fa_to_en(string: str) -> str:
    """Convert Persian digits to EN

    Usage::
    >>> from persiantools import digits
    >>> converted = digits.fa_to_en("۰۱۲۳۴۵۶۷۸۹")

    :param string: A string, will be converted
    :rtype: str
    """
    return utils.replace(string, FA_TO_EN_MAP)


def fa_to_ar(string: str) -> str:
    """Convert Persian digits to Arabic

    Usage::
    >>> from persiantools import digits
    >>> converted = digits.fa_to_ar("۰۱۲۳۴۵۶۷۸۹")

    :param string: A string, will be converted
    :rtype: str
    """
    return utils.replace(string, FA_TO_AR_MAP)


def _to_word(number: int, depth: bool) -> str:
    if number == 0:
        return ZERO if not depth else ""

    if number < 0:
        return NEGATIVE + _to_word(-number, depth)

    words = ""
    if depth:
        words = DELI
        depth = False

    for key in DECISION:
        if number < key:
            return words + DECISION[key](number, depth)

    raise OutOfRangeException("number must be lower than 1000000000000000")


def to_word(number: int) -> str:
    if not isinstance(number, int):
        raise TypeError("number must be integer")

    return _to_word(number, False)
