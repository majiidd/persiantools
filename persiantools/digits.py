from typing import Union

EN_TO_FA_MAP = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
AR_TO_FA_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩", "۰۱۲۳۴۵۶۷۸۹")
FA_TO_EN_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
FA_TO_AR_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "٠١٢٣٤٥٦٧٨٩")

ONES = ("یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه")
TENS = ("بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود")
HUNDREDS = ("یکصد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد")
RANGE = ("ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده")
BIG_RANGE = (" هزار", " میلیون", " میلیارد", " تریلیون")
MANTISSA = (
    "دهم",
    "صدم",
    "هزارم",
    "ده هزارم",
    "صد هزارم",
    "یک میلیونیم",
    "ده میلیونیم",
    "صد میلیونیم",
    "یک میلیاردم",
    "ده میلیاردم",
    "صد میلیاردم",
    "تریلیونیم",
    "ده تریلیونیم",
    "صد تریلیونیم",
)
ZERO = "صفر"
DELI = " و "
NEGATIVE = "منفی "

DECISION = {
    10: lambda n, depth: ONES[n - 1],
    20: lambda n, depth: RANGE[n - 10],
    100: lambda n, depth: TENS[n // 10 - 2] + _to_word(n % 10, True),
    1000: lambda n, depth: HUNDREDS[n // 100 - 1] + _to_word(n % 100, True),
    1_000_000: lambda n, depth: _to_word(n // 1_000, depth) + BIG_RANGE[0] + _to_word(n % 1_000, True),
    1_000_000_000: lambda n, depth: _to_word(n // 1_000_000, depth) + BIG_RANGE[1] + _to_word(n % 1_000_000, True),
    1_000_000_000_000: lambda n, depth: _to_word(n // 1_000_000_000, depth)
    + BIG_RANGE[2]
    + _to_word(n % 1_000_000_000, True),
    1_000_000_000_000_000: lambda n, depth: _to_word(n // 1_000_000_000_000, depth)
    + BIG_RANGE[3]
    + _to_word(n % 1_000_000_000_000, True),
}


class OutOfRangeException(Exception):
    pass


def en_to_fa(string: str) -> str:
    """
    Convert English digits to Persian digits.

    This function takes a string containing English digits and converts them to their
    corresponding Persian digits.

    Parameters:
    string (str): A string containing English digits to be converted.

    Returns:
    str: A string with English digits converted to Persian digits.

    Example:
    >>> from persiantools import digits
    >>> converted = digits.en_to_fa("0123456789")
    >>> print(converted)
    ۰۱۲۳۴۵۶۷۸۹
    """
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    return string.translate(EN_TO_FA_MAP)


def ar_to_fa(string: str) -> str:
    """
    Convert Arabic digits to Persian digits.

    This function takes a string containing Arabic digits and converts them to their
    corresponding Persian digits.

    Parameters:
    string (str): A string containing Arabic digits to be converted.

    Returns:
    str: A string with Arabic digits converted to Persian digits.

    Example:
    >>> from persiantools import digits
    >>> converted = digits.ar_to_fa("٠١٢٣٤٥٦٧٨٩")
    >>> print(converted)
    ۰۱۲۳۴۵۶۷۸۹
    """
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    return string.translate(AR_TO_FA_MAP)


def fa_to_en(string: str) -> str:
    """
    Convert Persian digits to English digits.

    This function takes a string containing Persian digits and converts them to their
    corresponding English digits.

    Parameters:
    string (str): A string containing Persian digits to be converted.

    Returns:
    str: A string with Persian digits converted to English digits.

    Example:
    >>> from persiantools import digits
    >>> converted = digits.fa_to_en("۰۱۲۳۴۵۶۷۸۹")
    >>> print(converted)
    0123456789
    """
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    return string.translate(FA_TO_EN_MAP)


def fa_to_ar(string: str) -> str:
    """
    Convert Persian digits to Arabic digits.

    This function takes a string containing Persian digits and converts them to their
    corresponding Arabic digits.

    Parameters:
    string (str): A string containing Persian digits to be converted.

    Returns:
    str: A string with Persian digits converted to Arabic digits.

    Example:
    >>> from persiantools import digits
    >>> converted = digits.fa_to_ar("۰۱۲۳۴۵۶۷۸۹")
    >>> print(converted)
    ٠١٢٣٤٥٦٧٨٩
    """
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    return string.translate(FA_TO_AR_MAP)


def _to_word(number: int, depth: bool) -> str:
    """
    Convert a number to its Persian word representation.

    This function takes an integer and converts it to its Persian word representation.
    It handles numbers up to 1,000,000,000,000,000 (one quadrillion).

    Parameters:
    number (int): The number to be converted.
    depth (bool): Indicates if the function is called recursively.

    Returns:
    str: The Persian word representation of the number.

    Raises:
    OutOfRangeException: If the number is outside the supported range.

    Example:
    >>> print(_to_word(123, False))
    یکصد و بیست و سه
    """
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


def _floating_number_to_word(number: float, depth: bool) -> str:
    """
    Convert a floating-point number to its Persian word representation.

    This function takes a floating-point number and converts it to its Persian word representation.
    It handles floating-point numbers up to 14 decimal places.

    Parameters:
    number (float): The floating-point number to be converted.
    depth (bool): A flag indicating if the function is called recursively.

    Returns:
    str: The Persian word representation of the floating-point number.

    Raises:
    OutOfRangeException: If the floating-point number has more than 14 decimal places.

    Example:
    >>> print(_floating_number_to_word(123.456, False))
    یکصد و بیست و سه و چهارصد و پنجاه و شش هزارم
    """
    left, right = str(abs(number)).split(".")
    if len(right) > 14:
        raise OutOfRangeException("You are allowed to use 14 digits for a floating point")

    if right.strip("0"):
        left_word = _to_word(int(left), False)
        mantissa_index = len(right.rstrip("0")) - 1
        if mantissa_index >= len(MANTISSA):
            raise ValueError("Fractional part is too long")
        result = (
            f"{left_word + DELI if left_word != ZERO else ''}{_to_word(int(right), False)} {MANTISSA[mantissa_index]}"
        )
        if number < 0:
            return NEGATIVE + result
        return result
    else:
        if number < 0:
            return NEGATIVE + _to_word(int(left), False)
        return _to_word(int(left), False)


def to_word(number: Union[int, float]) -> str:
    """
    Convert a number to its Persian word representation.

    This function converts both integers and floating-point numbers to their
    Persian word representations. It handles numbers up to 1 quadrillion (10^15)
    for integers and up to 14 decimal places for floating-point numbers.

    Parameters:
    number (float or int): The number to be converted. It can be an integer or a floating-point number.

    Returns:
    str: The Persian word representation of the number.

    Raises:
    OutOfRangeException: If the number is greater than or equal to 1 quadrillion (10^15) or if the
                         floating-point number has more than 14 decimal places.
    TypeError: If the input is not a float or an int.

    Examples:
    >>> digits.to_word(123)
    'یکصد و بیست و سه'

    >>> digits.to_word(123.456)
    'یکصد و بیست و سه و چهارصد و پنجاه و شش هزارم'
    """
    if isinstance(number, int):
        return _to_word(number, False)
    elif isinstance(number, float):
        return _floating_number_to_word(number, False)
    raise TypeError("number must be digit")
