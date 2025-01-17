import operator
import re
from datetime import date
from datetime import datetime as dt
from datetime import time as _time
from datetime import timedelta, timezone, tzinfo
from re import escape as re_escape

import pytz

from persiantools import digits, utils

# The minimum year supported by the JalaliDate module
MINYEAR = 1

# The maximum year supported by the JalaliDate module
MAXYEAR = 9377

# The maximum ordinal value supported by the JalaliDate module
_MAXORDINAL = 3424878

# Full month names in English for the Jalali calendar
MONTH_NAMES_EN = [
    None,
    "Farvardin",
    "Ordibehesht",
    "Khordad",
    "Tir",
    "Mordad",
    "Shahrivar",
    "Mehr",
    "Aban",
    "Azar",
    "Dey",
    "Bahman",
    "Esfand",
]

# Full month names in Persian for the Jalali calendar
MONTH_NAMES_FA = [
    None,
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]

# Abbreviated month names in English for the Jalali calendar
MONTH_NAMES_ABBR_EN = [
    None,
    "Far",
    "Ord",
    "Kho",
    "Tir",
    "Mor",
    "Sha",
    "Meh",
    "Aba",
    "Aza",
    "Dey",
    "Bah",
    "Esf",
]

# Abbreviated month names in Persian for the Jalali calendar
MONTH_NAMES_ABBR_FA = [
    None,
    "فرو",
    "ارد",
    "خرد",
    "تیر",
    "مرد",
    "شهر",
    "مهر",
    "آبا",
    "آذر",
    "دی",
    "بهم",
    "اسف",
]

# Full weekday names in English for the Jalali calendar
WEEKDAY_NAMES_EN = [
    "Shanbeh",
    "Yekshanbeh",
    "Doshanbeh",
    "Seshanbeh",
    "Chaharshanbeh",
    "Panjshanbeh",
    "Jomeh",
]

# Full weekday names in Persian for the Jalali calendar
WEEKDAY_NAMES_FA = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

# Abbreviated weekday names in English for the Jalali calendar
WEEKDAY_NAMES_ABBR_EN = ["Sha", "Yek", "Dos", "Ses", "Cha", "Pan", "Jom"]

# Abbreviated weekday names in Persian for the Jalali calendar
WEEKDAY_NAMES_ABBR_FA = ["ش", "ی", "د", "س", "چ", "پ", "ج"]

# The number of days in each month of the Jalali calendar.
# Each list contains the following columns:
# 1. The number of days in the month for a non-leap year.
# 2. The number of days in the month for a leap year.
# 3. The cumulative number of days from the start of the year to the start of the month (in a non-leap year).
# The first entry is for indexing purposes and is not used in calculations.
_MONTH_COUNT = [
    [-1, -1, -1],  # for indexing purposes
    [31, 31, 0],  # Farvardin
    [31, 31, 31],  # Ordibehesht
    [31, 31, 62],  # Khordad
    [31, 31, 93],  # Tir
    [31, 31, 124],  # Mordad
    [31, 31, 155],  # Shahrivar
    [30, 30, 186],  # Mehr
    [30, 30, 216],  # Aban
    [30, 30, 246],  # Azar
    [30, 30, 276],  # Dey
    [30, 30, 306],  # Bahman
    [29, 30, 336],  # Esfand
]

_FRACTION_CORRECTION = [100000, 10000, 1000, 100, 10]

# List of years that are exceptions to the 33-year leap year rule
# fmt: off
NON_LEAP_CORRECTION_SET = frozenset(
    [
        1502, 1601, 1634, 1667, 1700, 1733, 1766, 1799, 1832, 1865, 1898, 1931,
        1964, 1997, 2030, 2059, 2063, 2096, 2129, 2158, 2162, 2191, 2195, 2224,
        2228, 2257, 2261, 2290, 2294, 2323, 2327, 2356, 2360, 2389, 2393, 2422,
        2426, 2455, 2459, 2488, 2492, 2521, 2525, 2554, 2558, 2587, 2591, 2620,
        2624, 2653, 2657, 2686, 2690, 2719, 2723, 2748, 2752, 2756, 2781, 2785,
        2789, 2818, 2822, 2847, 2851, 2855, 2880, 2884, 2888, 2913, 2917, 2921,
        2946, 2950, 2954, 2979, 2983, 2987,
    ]
)
# fmt: on

MIN_NON_LEAP_CORRECTION = 1502


def _is_ascii_digit(c: str) -> bool:
    return c in "0123456789"


class JalaliDate:
    """
    Represents a date in the Jalali (Persian) calendar.

    Attributes:
        year (int): The year of the Jalali date.
        month (int): The month of the Jalali date.
        day (int): The day of the Jalali date.
        locale (str): The locale for the Jalali date ('en' or 'fa').
    """

    # Using __slots__ to declare a fixed set of attributes for the JalaliDate class.
    # This helps to save memory by preventing the creation of a __dict__ for each instance.
    # The attributes are:
    # _year: The year of the Jalali date.
    # _month: The month of the Jalali date.
    # _day: The day of the Jalali date.
    # _locale: The locale for the date representation (e.g., 'en' or 'fa').
    # _hashcode: Cached hash code for the instance to speed up hash-based operations.
    __slots__ = "_year", "_month", "_day", "_locale", "_hashcode"

    def __init__(self, year, month=None, day=None, locale="en"):
        """
        Initialize a JalaliDate object.

        Args:
            year (int, JalaliDate, datetime.date, bytes, or str): The year of the Jalali date. It can also be:
                - An instance of JalaliDate.
                - An instance of datetime.date.
                - A 4-byte representation of the date.
                - A string that starts with '['.
            month (int, optional): The month of the Jalali date. Default is None.
            day (int, optional): The day of the Jalali date. Default is None.
            locale (str, optional): The locale for the date representation. It must be 'en' or 'fa'. Default is 'en'.

        Raises:
            ValueError: If the locale is not 'en' or 'fa'.

        Notes:
            - If `year` is an instance of JalaliDate and `month` is None, the date will be initialized with the values from the JalaliDate instance.
            - If `year` is an instance of datetime.date, the date will be converted to Jalali date.
            - If `year` is a 4-byte representation or a string starting with '[', the state will be set from these representations.

        """
        if locale not in ["en", "fa"]:
            raise ValueError("locale must be 'en' or 'fa'")

        if isinstance(year, JalaliDate) and month is None:
            year, month, day, locale = year.year, year.month, year.day, year.locale

        elif isinstance(year, date):
            jdate = self.to_jalali(year)
            year, month, day = jdate.year, jdate.month, jdate.day

        elif (isinstance(year, bytes) and len(year) == 4 and 1 <= year[2] <= 12) or (
            isinstance(year, str) and year.startswith("[", 0, 1)
        ):
            self.__setstate__(year)

            year, month, day = self._year, self._month, self._day

        self._year, self._month, self._day, self._locale = self._check_date_fields(year, month, day, locale)
        self._hashcode = -1

    @property
    def year(self) -> int:
        """
        Get the year component of the date.

        Returns:
            int: The year as an integer.
        """
        return self._year

    @property
    def month(self) -> int:
        """
        Get the month component of the date.

        Returns:
            int: The month as an integer.
        """
        return self._month

    @property
    def day(self) -> int:
        """
        Get the day of the month.

        Returns:
            int: The day of the month.
        """
        return self._day

    @property
    def locale(self):
        """
        Get the locale setting for the current instance.

        Returns:
            str: The locale setting.
        """
        return self._locale

    @locale.setter
    def locale(self, locale: str):
        if locale not in ("en", "fa"):
            raise ValueError("locale must be 'en' or 'fa'")

        self._locale = locale

    @classmethod
    def _check_date_fields(cls, year: int, month: int, day: int, locale: str):
        """
        Validate and normalize the date fields.

        Args:
            year (int): The year of the Jalali date.
            month (int): The month of the Jalali date.
            day (int): The day of the Jalali date.
            locale (str): The locale for the date representation. It must be 'en' or 'fa'.

        Returns:
            tuple: A tuple containing validated and normalized year, month, day, and locale.

        Raises:
            ValueError: If the provided date fields are not valid.
        """
        year = operator.index(year)
        month = operator.index(month)
        day = operator.index(day)

        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError(f"year must be in {MINYEAR}..{MAXYEAR}", year)

        if not 1 <= month <= 12:
            raise ValueError("month must be in 1..12", month)

        dim = cls.days_in_month(month, year)
        if not 1 <= day <= dim:
            raise ValueError(f"day must be in 1..{dim}", day)

        if locale not in ["en", "fa"]:
            raise ValueError("locale must be 'en' or 'fa'")

        return year, month, day, locale

    @classmethod
    def check_date(cls, year: int, month: int, day: int) -> bool:
        """
        Check if the given Jalali date fields constitute a valid date.

        Args:
            year (int): The year of the Jalali date.
            month (int): The month of the Jalali date (1 through 12).
            day (int): The day of the Jalali date (1 through 31, depending on the month).

        Returns:
            bool: True if the provided date fields constitute a valid Jalali date, False otherwise.

        Notes:
            - This method checks whether the given year, month, and day form a valid Jalali date.
            - It considers the specific rules for leap years in the Jalali calendar.
        """
        try:
            cls._check_date_fields(year, month, day, "en")
        except (ValueError, TypeError):
            return False
        else:
            return True

    @staticmethod
    def is_leap(year: int) -> bool:
        """
        Determines if a given Persian year is a leap year using the 33-year rule,
        with corrections for specific years that deviate from the rule.

        This function is based on the Rust implementation from the ICU4X project:
        https://github.com/unicode-org/icu4x/blob/main/utils/calendrical_calculations/src/persian.rs

        Args:
            year (int): The Persian year to check.

        Returns:
            bool: True if the year is a leap year, False otherwise.
        """
        if not (MINYEAR <= year <= MAXYEAR):
            raise ValueError(f"Year must be between {MINYEAR} and {MAXYEAR}")

        if year < MIN_NON_LEAP_CORRECTION:
            return (25 * year + 11) % 33 < 8

        if year in NON_LEAP_CORRECTION_SET:
            return False

        if (year - 1) in NON_LEAP_CORRECTION_SET:
            return True

        return (25 * year + 11) % 33 < 8

    @classmethod
    def days_in_month(cls, month: int, year: int) -> int:
        """
        Get the number of days in a given month for a specified year.

        Args:
            month (int): The month (1-12).
            year (int): The year.

        Returns:
            int: The number of days in the month.

        Raises:
            AssertionError: If the month is out of the valid range.
        """
        if not 1 <= month <= 12:
            raise ValueError("month must be in 1..12")

        if month == 12 and cls.is_leap(year):
            return _MONTH_COUNT[month][1]

        return _MONTH_COUNT[month][0]

    @staticmethod
    def days_before_month(month: int) -> int:
        """
        Get the number of days before the start of a given month.

        Args:
            month (int): The month (1-12).

        Returns:
            int: The number of days before the month.

        Raises:
            AssertionError: If the month is out of the valid range.
        """
        if not 1 <= month <= 12:
            raise ValueError("month must be in 1..12")

        return _MONTH_COUNT[month][2]

    @classmethod
    def to_jalali(cls, year, month=None, day=None):
        """
        Convert a Gregorian date to a Jalali (Persian) date.

        This method converts a given Gregorian date (or a datetime.date object) to its
        corresponding Jalali (Persian) date. If a datetime.date object is provided,
        the month and day parameters are automatically extracted.

        Parameters:
        year (int or datetime.date): The year of the Gregorian date, or a datetime.date object.
        month (int, optional): The month of the Gregorian date.
        day (int, optional): The day of the Gregorian date.

        Returns:
        JalaliDate: A JalaliDate object representing the corresponding Jalali date.

        Example:
        >>> g_date = date(2021, 3, 21)
        >>> j_date = JalaliDate.to_jalali(g_date)
        >>> print(j_date)
        JalaliDate(1400, 1, 1)

        >>> j_date = JalaliDate.to_jalali(2021, 3, 21)
        >>> print(j_date)
        JalaliDate(1400, 1, 1)
        """
        if month is None and isinstance(year, date):
            month = year.month
            day = year.day
            year = year.year

        # Days in each month of the Gregorian calendar
        gregorian_days_in_month = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

        # Determine the Jalali year
        jalali_year = 0 if year <= 1600 else 979
        year -= 621 if year <= 1600 else 1600

        # Determine if the year is a leap year
        leap_year = year + 1 if month > 2 else year

        # Calculate the number of days
        days = (365 * year) + (leap_year + 3) // 4 - (leap_year + 99) // 100
        days += (leap_year + 399) // 400 - 80 + day + gregorian_days_in_month[month - 1]

        # Update the Jalali year
        jalali_year += 33 * (days // 12053)
        days %= 12053
        jalali_year += 4 * (days // 1461)
        days %= 1461

        # Correct for the leap year case
        if days > 365:
            jalali_year += (days - 1) // 365
            days = (days - 1) % 365

        # Determine the Jalali month and day
        if days < 186:
            jalali_month = 1 + days // 31
            jalali_day = 1 + (days % 31)
        else:
            days -= 186
            jalali_month = 7 + days // 30
            jalali_day = 1 + (days % 30)

        return cls(jalali_year, jalali_month, jalali_day)

    def to_gregorian(self) -> date:
        """
        Convert a Jalali (Persian) date to a Gregorian date.

        This method converts the current Jalali (Persian) date instance to its
        corresponding Gregorian date.

        Returns:
        date: A datetime.date object representing the corresponding Gregorian date.

        Example:
        >>> j_date = JalaliDate(1400, 1, 1)
        >>> g_date = j_date.to_gregorian()
        >>> print(g_date)
        2021-03-21
        """
        year = self.year + 1595
        month = self.month
        day = self.day

        # Calculate the total number of days
        days = -355668 + (365 * year) + ((year // 33) * 8) + (((year % 33) + 3) // 4) + day
        if month < 7:
            days += (month - 1) * 31
        else:
            days += ((month - 7) * 30) + 186

        # Determine the Gregorian year
        gregorian_year = 400 * (days // 146097)
        days %= 146097

        if days > 36524:
            days -= 1
            gregorian_year += 100 * (days // 36524)
            days %= 36524
            if days >= 365:
                days += 1

        gregorian_year += 4 * (days // 1461)
        days %= 1461
        if days > 365:
            gregorian_year += (days - 1) // 365
            days = (days - 1) % 365

        gregorian_day = days + 1

        # Handle leap years for February day count adjustment
        if (gregorian_year % 4 == 0 and gregorian_year % 100 != 0) or (gregorian_year % 400 == 0):
            feb_days = 29
        else:
            feb_days = 28

        # Days in each month of the Gregorian calendar
        gregorian_days_in_month = [0, 31, feb_days, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # Determine the Gregorian month
        gregorian_month = 1
        for days_in_month in gregorian_days_in_month[1:]:
            if gregorian_day <= days_in_month:
                break
            gregorian_day -= days_in_month
            gregorian_month += 1

        return date(gregorian_year, gregorian_month, gregorian_day)

    @classmethod
    def today(cls):
        """
        Get the current date in the Jalali (Persian) calendar.

        This method returns a JalaliDate object representing the current date,
        based on the system's local time.

        Returns:
            JalaliDate: A JalaliDate object representing today's date.

        Example:
            >>> j_date = JalaliDate.today()
            >>> print(j_date)
        """
        return cls(date.today())

    def timetuple(self):
        """
        Return the Jalali date as a time.struct_time object.

        This method returns the Jalali date as a struct_time object, which is
        similar to the output of the `time.localtime()` or `time.gmtime()` functions.
        It contains year, month, day, hour, minute, second, weekday, Julian day, and DST flag.

        Returns:
            struct_time: A time.struct_time object representing the Jalali date.

        Example:
            >>> from persiantools.jdatetime import JalaliDate
            >>> jdate = JalaliDate(1398, 3, 17)
            >>> jdate.timetuple()
            time.struct_time(tm_year=2019, tm_mon=6, tm_mday=7, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=158, tm_isdst=-1)
        """
        return self.to_gregorian().timetuple()

    def isoformat(self) -> str:
        """
        Return the Jalali date as a string in ISO 8601 format.

        This method returns the Jalali date as a string formatted according to the
        ISO 8601 standard, which is `YYYY-MM-DD`.

        Returns:
            str: The Jalali date in ISO 8601 format.

        Example:
            >>> from persiantools.jdatetime import JalaliDate
            >>> jdate = JalaliDate(1398, 3, 17)
            >>> jdate.isoformat()
            '1398-03-17'
        """
        iso = f"{self._year:04d}-{self._month:02d}-{self._day:02d}"

        if self._locale == "fa":
            iso = digits.en_to_fa(iso)

        return iso

    __str__ = isoformat

    def toordinal(self) -> int:
        return self.to_gregorian().toordinal() - 226894

    @classmethod
    def fromordinal(cls, n: int):
        return cls(date.fromordinal(n + 226894))

    @classmethod
    def fromisoformat(cls, date_string: str):
        """
        Construct a JalaliDate from an ISO 8601 formatted date string.

        Args:
            date_string (str): The date string in ISO 8601 format.

        Returns:
            JalaliDate: A JalaliDate object corresponding to the given date string.

        Raises:
            TypeError: If the provided argument is not a string.
            ValueError: If the provided string is not a valid ISO 8601 formatted date.
        """
        if not isinstance(date_string, str):
            raise TypeError("fromisoformat: argument must be str")

        if len(date_string) not in (7, 8, 10):
            raise ValueError(f"Invalid isoformat string: {date_string!r}")

        try:
            return cls(*cls._parse_isoformat_date(digits.fa_to_en(date_string)))
        except Exception:
            raise ValueError(f"Invalid isoformat string: {date_string!r}")

    @classmethod
    def _parse_isoformat_date(cls, dtstr: str):
        # It is assumed that this function will only be called with a
        # string of length exactly 10, and (though this is not used) ASCII-only
        assert len(dtstr) in (7, 8, 10)

        year = int(dtstr[0:4])
        if dtstr[4] != "-":
            raise ValueError(f"Invalid date separator: {dtstr[4]}")

        month = int(dtstr[5:7])

        if dtstr[7] != "-":
            raise ValueError("Invalid date separator")

        day = int(dtstr[8:10])

        return [year, month, day]

    def __hash__(self):
        if self._hashcode == -1:
            self._hashcode = hash(self.__getstate__())

        return self._hashcode

    def __getstate__(self):
        yhi, ylo = divmod(self._year, 256)
        return (bytes([yhi, ylo, self._month, self._day]),)

    def __setstate__(self, string):
        if len(string) != 4 or not (1 <= string[2] <= 12):
            raise TypeError("not enough arguments")

        yhi, ylo, self._month, self._day = string
        self._year = yhi * 256 + ylo

    def __reduce__(self):
        return self.__class__, self.__getstate__()

    def __repr__(self):
        return f"JalaliDate({self._year}, {self._month}, {self._day}, {WEEKDAY_NAMES_EN[self.weekday()]})"

    resolution = timedelta(1)

    def replace(self, year=None, month=None, day=None, locale=None):
        """
        Return a new JalaliDate instance with one or more of the specified fields replaced.

        This method allows for the replacement of the year, month, day, or locale
        of an existing JalaliDate instance. If a field is not specified, the current
        value of that field is retained.

        Args:
            year (int, optional): The new year value. Defaults to None.
            month (int, optional): The new month value. Defaults to None.
            day (int, optional): The new day value. Defaults to None.
            locale (str, optional): The new locale value ('en' or 'fa'). Defaults to None.

        Returns:
            JalaliDate: A new JalaliDate instance with the specified fields replaced.

        Example:
            >>> jdate = JalaliDate(1400, 1, 1)
            >>> new_jdate = jdate.replace(month=2)
            >>> new_jdate
            JalaliDate(1400, 2, 1)
        """
        if year is None:
            year = self._year

        if month is None:
            month = self._month

        if day is None:
            day = self._day

        if locale is None:
            locale = self._locale

        return JalaliDate(year, month, day, locale)

    @classmethod
    def fromtimestamp(cls, timestamp: float):
        return cls(date.fromtimestamp(timestamp))

    def weekday(self) -> int:
        """
        Returns the day of the week as an integer.

        The days of the week are represented as follows:
        0 - Shanbeh
        1 - Yekshanbeh
        2 - Doshanbeh
        3 - Seshanbeh
        4 - Chaharshanbeh
        5 - Panjshanbeh
        6 - Jomeh

        Returns:
            int: An integer representing the day of the week.
        """
        return (self.toordinal() + 4) % 7

    def __format__(self, fmt: str):
        if not isinstance(fmt, str):
            raise TypeError(f"must be str, not {type(fmt).__name__}")
        if len(fmt) != 0:
            return self.strftime(fmt)

        return str(self)

    def isoweekday(self) -> int:
        """
        Return the ISO weekday.

        The ISO weekday is a number representing the day of the week, where Shanbeh is 1 and Jomeh is 7.

        Returns:
            int: An integer representing the ISO weekday.
        """
        return self.weekday() + 1

    def week_of_year(self) -> int:
        """
        Calculate the week number of the year for the current Jalali date.

        Returns:
            int: The week number of the year, starting from 1.
        """
        o = JalaliDate(self._year, 1, 1).weekday()
        days = self.days_before_month(self._month) + self._day + o

        week_no, r = divmod(days, 7)

        if r > 0:
            week_no += 1

        return week_no

    def isocalendar(self):
        """
        Return a 3-tuple containing ISO year, week number, and weekday.

        Returns:
            tuple: A tuple containing the ISO year, ISO week number, and ISO weekday.
        """
        return self.year, self.week_of_year(), self.isoweekday()

    def ctime(self) -> str:
        """
        Return a string representing the date and time in a locale’s appropriate format.

        This method uses the strftime() function with the format code "%c" to generate
        a string representation of the date and time.

        Returns:
            str: A string representing the date and time.
        """
        return self.strftime("%c")

    def strftime(self, fmt: str, locale=None) -> str:
        """
        Format a Jalali date according to the given format string.

        This method returns a string representing the Jalali date, controlled by an explicit format string.
        It is similar to the `strftime` method used with `datetime` objects.

        Args:
            fmt (str): The format string.
            locale (str, optional): The locale to use for formatting ('en' for English or 'fa' for Persian).
                                    If None, the instance's locale is used.

        Returns:
            str: The formatted date string.

        Example:
            >>> j_date = JalaliDate(1400, 1, 1)
            >>> j_date.strftime("%A, %d %B %Y")
            'Yekshanbeh, 01 Farvardin 1400'

            >>> j_date.strftime("%A, %d %B %Y", locale="fa")
            'یکشنبه, ۰۱ فروردین ۱۴۰۰'
        """
        if locale is None or locale not in ["fa", "en"]:
            locale = self._locale

        month_names = MONTH_NAMES_EN if locale == "en" else MONTH_NAMES_FA
        month_names_abbr = MONTH_NAMES_ABBR_EN if locale == "en" else MONTH_NAMES_ABBR_FA
        day_names = WEEKDAY_NAMES_EN if locale == "en" else WEEKDAY_NAMES_FA
        day_names_abbr = WEEKDAY_NAMES_ABBR_EN if locale == "en" else WEEKDAY_NAMES_ABBR_FA
        am = "AM" if locale == "en" else "ق.ظ"

        format_time = {
            "%a": day_names_abbr[self.weekday()],
            "%A": day_names[self.weekday()],
            "%w": str(self.weekday()),
            "%d": f"{self._day:02d}",
            "%b": month_names_abbr[self._month],
            "%B": month_names[self._month],
            "%m": f"{self._month:02d}",
            "%y": f"{self._year % 100:02d}",
            "%Y": f"{self._year:04d}",
            "%H": "00",
            "%I": "00",
            "%p": am,
            "%M": "00",
            "%S": "00",
            "%f": "000000",
            "%z": "",
            "%Z": "",
            "%j": f"{self.days_before_month(self._month) + self._day:03d}",
            "%U": f"{self.week_of_year():02d}",
            "%W": f"{self.week_of_year():02d}",
            "%X": "00:00:00",
            "%%": "%",
        }

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": "%A %d %B %Y"})

        if "%x" in fmt:
            fmt = utils.replace(fmt, {"%x": "%y/%m/%d"})

        result = utils.replace(fmt, format_time)

        if locale == "fa":
            result = digits.en_to_fa(result)

        return result

    def _compare(self, other):
        assert isinstance(other, JalaliDate)

        y, m, d = self._year, self._month, self._day
        y2, m2, d2 = other.year, other.month, other.day

        return 0 if (y, m, d) == (y2, m2, d2) else 1 if (y, m, d) > (y2, m2, d2) else -1

    def __eq__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) == 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) == 0

        return False

    def __ne__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) != 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) != 0

        return True

    def __le__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) <= 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) <= 0

        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) < 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) < 0

        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) >= 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) >= 0

        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) > 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) > 0

        raise NotImplementedError

    def __add__(self, other):
        "Add a date to a timedelta."
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days

            if 0 < o <= _MAXORDINAL:
                return JalaliDate.fromordinal(o)

            raise OverflowError("result out of range")

        raise NotImplementedError

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self + timedelta(-other.days)

        if isinstance(other, JalaliDate):
            days1 = self.toordinal()
            days2 = other.toordinal()

            return timedelta(days1 - days2)

        if isinstance(other, date):
            days1 = self.toordinal()
            days2 = JalaliDate(other).toordinal()

            return timedelta(days1 - days2)

        raise NotImplementedError

    @classmethod
    def strptime(cls, data_string, fmt):
        raise NotImplementedError


_tzinfo_class = tzinfo


class JalaliDateTime(JalaliDate):
    __slots__ = JalaliDate.__slots__ + ("_hour", "_minute", "_second", "_microsecond", "_tzinfo")

    def __init__(
        self,
        year,
        month=None,
        day=None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None,
        locale="en",
    ):
        # Pickle support

        if isinstance(year, JalaliDateTime) and month is None:
            month = year.month
            day = year.day
            hour = year.hour
            minute = year.minute
            second = year.second
            microsecond = year.microsecond
            year = year.year

        elif isinstance(year, dt) and month is None:
            j = JalaliDate(year.date())
            month = j.month
            day = j.day
            hour = year.hour
            minute = year.minute
            second = year.second
            microsecond = year.microsecond

            if tzinfo is None:
                tzinfo = year.tzinfo

            year = j.year

        elif (isinstance(year, bytes) and len(year) == 10) or (isinstance(year, str) and year.startswith("[", 0, 1)):
            self.__setstate__(year, month)

            year = self._year
            month = self._month
            day = self._day
            hour = self._hour
            minute = self._minute
            second = self._second
            microsecond = self._microsecond
            tzinfo = self._tzinfo

        super().__init__(year, month, day, locale)
        self._check_tzinfo_arg(tzinfo)
        self._check_time_fields(hour, minute, second, microsecond)

        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo

    @staticmethod
    def _check_time_fields(hour, minute, second, microsecond):
        if not isinstance(hour, int):
            raise TypeError("int expected")

        if not 0 <= hour <= 23:
            raise ValueError("hour must be in 0..23", hour)

        if not 0 <= minute <= 59:
            raise ValueError("minute must be in 0..59", minute)

        if not 0 <= second <= 59:
            raise ValueError("second must be in 0..59", second)

        if not 0 <= microsecond <= 999999:
            raise ValueError("microsecond must be in 0..999999", microsecond)

    @property
    def hour(self) -> int:
        """
        Get the hour component of the datetime.

        Returns:
            int: The hour component of the datetime.
        """
        return self._hour

    @property
    def minute(self) -> int:
        """
        Get the minute component of the datetime.

        Returns:
            int: The minute component of the datetime.
        """
        return self._minute

    @property
    def second(self) -> int:
        """
        Get the second component of the time.

        Returns:
            int: The second component of the time.
        """
        return self._second

    @property
    def microsecond(self) -> int:
        """
        Returns the microsecond component of the datetime.

        Returns:
            int: The microsecond component of the datetime.
        """
        return self._microsecond

    @property
    def tzinfo(self):
        """
        Returns the time zone information associated with this datetime object.

        :return: The time zone information.
        :rtype: tzinfo
        """
        return self._tzinfo

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        return cls(dt.fromtimestamp(t, tz))

    @classmethod
    def utcfromtimestamp(cls, t):
        return cls(dt.fromtimestamp(t, tz=timezone.utc))

    def date(self):
        return JalaliDate(self.year, self.month, self.day).to_gregorian()

    def jalali_date(self):
        return JalaliDate(self.year, self.month, self.day)

    def jdate(self):
        return self.jalali_date()

    def time(self):
        return _time(self.hour, self.minute, self.second, self.microsecond)

    def timetz(self):
        return _time(self.hour, self.minute, self.second, self.microsecond, self.tzinfo)

    def replace(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        tzinfo=True,
        locale=None,
    ):

        if year is None:
            year = self.year

        if month is None:
            month = self.month

        if day is None:
            day = self.day

        if hour is None:
            hour = self.hour

        if minute is None:
            minute = self.minute

        if second is None:
            second = self.second

        if microsecond is None:
            microsecond = self.microsecond

        if tzinfo is True:
            tzinfo = self.tzinfo

        if locale is None:
            locale = self.locale

        self._check_date_fields(year, month, day, locale)
        self._check_time_fields(hour, minute, second, microsecond)
        self._check_tzinfo_arg(tzinfo)

        return JalaliDateTime(year, month, day, hour, minute, second, microsecond, tzinfo, locale)

    @classmethod
    def now(cls, tz=None):
        return cls(dt.now(tz))

    @classmethod
    def today(cls):
        return cls.now()

    @classmethod
    def utcnow(cls):
        return cls(dt.now(tz=timezone.utc))

    @classmethod
    def fromisoformat(cls, date_string: str):
        """Construct a datetime from a string in one of the ISO 8601 formats."""
        if not isinstance(date_string, str):
            raise TypeError("fromisoformat: argument must be str")

        if len(date_string) < 7:
            raise ValueError(f"Invalid isoformat string: {date_string!r}")

        # Split this at the separator
        try:
            separator_location = cls._find_isoformat_datetime_separator(date_string)
            dstr = date_string[0:separator_location]
            tstr = date_string[(separator_location + 1) :]

            date_components = cls._parse_isoformat_date(dstr)
        except ValueError:
            raise ValueError(f"Invalid isoformat string: {date_string!r}") from None

        if tstr:
            try:
                time_components = cls._parse_isoformat_time(tstr)
            except ValueError:
                raise ValueError(f"Invalid isoformat string: {date_string!r}") from None
        else:
            time_components = [0, 0, 0, 0, None]

        return cls(*(date_components + time_components))

    @classmethod
    def _find_isoformat_datetime_separator(cls, dtstr: str):
        # See the comment in _datetimemodule.c:_find_isoformat_datetime_separator
        len_dtstr = len(dtstr)
        if len_dtstr == 7:
            return 7

        assert len_dtstr > 7
        date_separator = "-"
        week_indicator = "W"

        if dtstr[4] == date_separator:
            if dtstr[5] == week_indicator:
                if len_dtstr < 8:
                    raise ValueError("Invalid ISO string")
                if len_dtstr > 8 and dtstr[8] == date_separator:
                    if len_dtstr == 9:
                        raise ValueError("Invalid ISO string")
                    if len_dtstr > 10 and _is_ascii_digit(dtstr[10]):
                        # This is as far as we need to resolve the ambiguity for
                        # the moment - if we have YYYY-Www-##, the separator is
                        # either a hyphen at 8 or a number at 10.
                        #
                        # We'll assume it's a hyphen at 8 because it's way more
                        # likely that someone will use a hyphen as a separator than
                        # a number, but at this point it's really best effort
                        # because this is an extension of the spec anyway.
                        # TODO(pganssle): Document this
                        return 8
                    return 10
                else:
                    # YYYY-Www (8)
                    return 8
            else:
                # YYYY-MM-DD (10)
                return 10
        else:
            if dtstr[4] == week_indicator:
                # YYYYWww (7) or YYYYWwwd (8)
                idx = 7
                while idx < len_dtstr:
                    if not _is_ascii_digit(dtstr[idx]):
                        break
                    idx += 1

                if idx < 9:
                    return idx

                if idx % 2 == 0:
                    # If the index of the last number is even, it's YYYYWwwd
                    return 7
                else:
                    return 8
            else:
                # YYYYMMDD (8)
                return 8

    @classmethod
    def _parse_isoformat_time(cls, tstr: str):
        # Format supported is HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]
        len_str = len(tstr)
        if len_str < 2:
            raise ValueError("Isoformat time too short")

        # This is equivalent to re.search('[+-Z]', tstr), but faster
        tz_pos = tstr.find("-") + 1 or tstr.find("+") + 1 or tstr.find("Z") + 1
        timestr = tstr[: tz_pos - 1] if tz_pos > 0 else tstr

        time_comps = cls._parse_hh_mm_ss_ff(timestr)

        tzi = None
        if tz_pos == len_str and tstr[-1] == "Z":
            tzi = timezone.utc
        elif tz_pos > 0:
            tzstr = tstr[tz_pos:]

            # Valid time zone strings are:
            # HH                  len: 2
            # HHMM                len: 4
            # HH:MM               len: 5
            # HHMMSS              len: 6
            # HHMMSS.f+           len: 7+
            # HH:MM:SS            len: 8
            # HH:MM:SS.f+         len: 10+

            if len(tzstr) in (0, 1, 3):
                raise ValueError("Malformed time zone string")

            tz_comps = cls._parse_hh_mm_ss_ff(tzstr)

            if all(x == 0 for x in tz_comps):
                tzi = timezone.utc
            else:
                tzsign = -1 if tstr[tz_pos - 1] == "-" else 1

                td = timedelta(hours=tz_comps[0], minutes=tz_comps[1], seconds=tz_comps[2], microseconds=tz_comps[3])

                tzi = timezone(tzsign * td)

        time_comps.append(tzi)

        return time_comps

    @classmethod
    def _parse_hh_mm_ss_ff(cls, tstr: str):
        # Parses things of the form HH[:?MM[:?SS[{.,}fff[fff]]]]
        len_str = len(tstr)

        time_comps = [0, 0, 0, 0]
        pos = 0
        for comp in range(0, 3):
            if (len_str - pos) < 2:
                raise ValueError("Incomplete time component")

            time_comps[comp] = int(tstr[pos : pos + 2])

            pos += 2
            next_char = tstr[pos : pos + 1]

            if comp == 0:
                has_sep = next_char == ":"

            if not next_char or comp >= 2:
                break

            if has_sep and next_char != ":":
                raise ValueError("Invalid time separator: %c" % next_char)

            pos += has_sep

        if pos < len_str:
            if tstr[pos] not in ".,":
                raise ValueError("Invalid microsecond component")
            else:
                pos += 1

                len_remainder = len_str - pos

                if len_remainder >= 6:
                    to_parse = 6
                else:
                    to_parse = len_remainder

                time_comps[3] = int(tstr[pos : (pos + to_parse)])
                if to_parse < 6:
                    time_comps[3] *= _FRACTION_CORRECTION[to_parse - 1]
                if len_remainder > to_parse and not all(map(_is_ascii_digit, tstr[(pos + to_parse) :])):
                    raise ValueError("Non-digit values in unparsed fraction")

        return time_comps

    @staticmethod
    def _check_tzinfo_arg(tz):
        if tz is not None and not isinstance(tz, tzinfo):
            raise TypeError("tzinfo argument must be None or of a tzinfo subclass")

    @classmethod
    def combine(cls, jdate, time_v):
        if not isinstance(jdate, JalaliDate):
            raise TypeError("date argument must be a JalaliDate instance")

        if not isinstance(time_v, _time):
            raise TypeError("time argument must be a time instance")

        return cls(
            jdate.year,
            jdate.month,
            jdate.day,
            time_v.hour,
            time_v.minute,
            time_v.second,
            time_v.microsecond,
            time_v.tzinfo,
        )

    def timestamp(self):
        return self.to_gregorian().timestamp()

    def utctimetuple(self):
        "Return UTC time tuple compatible with time.gmtime()."
        return self.to_gregorian().utctimetuple()

    def astimezone(self, tz=None):
        """
        Convert the current JalaliDateTime to another timezone.

        This method returns a new JalaliDateTime object representing the same
        time instant in a different timezone. The returned object will have
        its `tzinfo` attribute set to the new timezone.

        Parameters:
        tz (tzinfo, optional): The timezone to convert the JalaliDateTime to.
                            If `None`, the method will use the system's local timezone.
                            The `tz` parameter must be an instance of a subclass of `datetime.tzinfo`.

        Returns:
        JalaliDateTime: A new JalaliDateTime object with the same time instant in the specified timezone.

        Raises:
        TypeError: If the `tz` parameter is not `None` and is not an instance of a subclass of `datetime.tzinfo`.

        Example:
        >>> from datetime import timezone, timedelta
        >>> jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=3)))
        >>> jdt_utc = jdt.astimezone(timezone.utc)
        >>> print(jdt_utc)
        JalaliDateTime(1400, 1, 1, 9, 30, 45, tzinfo=datetime.timezone.utc)

        >>> new_tz = timezone(timedelta(hours=5))
        >>> jdt_new_tz = jdt.astimezone(new_tz)
        >>> print(jdt_new_tz)
        JalaliDateTime(1400, 1, 1, 17, 30, 45, tzinfo=datetime.timezone(datetime.timedelta(seconds=18000)))
        """
        return JalaliDateTime(self.to_gregorian().astimezone(tz))

    def ctime(self):
        month_names = MONTH_NAMES_EN if self.locale == "en" else MONTH_NAMES_FA
        day_names = WEEKDAY_NAMES_EN if self.locale == "en" else WEEKDAY_NAMES_FA

        c = "%s %02d %s %d %02d:%02d:%02d" % (
            day_names[self.weekday()],
            self.day,
            month_names[self.month],
            self.year,
            self.hour,
            self.minute,
            self.second,
        )

        if self.locale == "fa":
            c = digits.en_to_fa(c)

        return c

    def isoformat(self, sep="T") -> str:
        s = "%04d-%02d-%02d%c%02d:%02d:%02d" % (
            self.year,
            self.month,
            self.day,
            sep,
            self.hour,
            self.minute,
            self.second,
        )

        if self.microsecond:
            s += ".%06d" % self.microsecond

        off = self.utcoffset()
        if off is not None:
            if off.days < 0:
                sign = "-"
                off = -off
            else:
                sign = "+"
            hh, mm = divmod(off.total_seconds(), timedelta(hours=1).total_seconds())
            assert not mm % timedelta(minutes=1).total_seconds(), "whole minute"
            mm //= timedelta(minutes=1).total_seconds()
            s += "%s%02d:%02d" % (sign, hh, mm)
        return s

    def utcoffset(self):
        if self._tzinfo is None:
            return None

        offset = self._tzinfo.utcoffset(self.to_gregorian())

        return offset

    def tzname(self):
        if self._tzinfo is None:
            return None

        name = self._tzinfo.tzname(self.to_gregorian())

        if name is not None and not isinstance(name, str):
            raise TypeError("tzinfo.tzname() must return None or string, " "not '%s'" % type(name))

        return name

    def dst(self):
        if self._tzinfo is None:
            return None

        offset = self._tzinfo.dst(self.to_gregorian())
        self.check_utc_offset("dst", offset)

        return offset

    @staticmethod
    def check_utc_offset(name, offset):
        assert name in ("utcoffset", "dst")

        if offset is None:
            return

        if not isinstance(offset, timedelta):
            raise TypeError("tzinfo.%s() must return None " "or timedelta, not '%s'" % (name, type(offset)))

        if offset % timedelta(minutes=1) or offset.microseconds:
            raise ValueError("tzinfo.%s() must return a whole number " "of minutes, got %s" % (name, offset))

        if not -timedelta(1) < offset < timedelta(1):
            raise ValueError(
                "%s()=%s, must be must be strictly between"
                " -timedelta(hours=24) and timedelta(hours=24)" % (name, offset)
            )

    @classmethod
    def to_jalali(
        cls,
        year,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        tzinfo=None,
    ):
        """
        Convert a Gregorian date or datetime to a Jalali (Persian) datetime.

        This method converts a given Gregorian date or datetime to its corresponding
        Jalali (Persian) date or datetime. The conversion considers all date and time
        components, including year, month, day, hour, minute, second, and microsecond.

        Parameters:
        year (int or datetime): The year of the Gregorian date, or a datetime object.
        month (int, optional): The month of the Gregorian date.
        day (int, optional): The day of the Gregorian date.
        hour (int, optional): The hour of the Gregorian datetime.
        minute (int, optional): The minute of the Gregorian datetime.
        second (int, optional): The second of the Gregorian datetime.
        microsecond (int, optional): The microsecond of the Gregorian datetime.
        tzinfo (tzinfo, optional): The timezone information.

        Returns:
        JalaliDateTime: A JalaliDateTime object representing the corresponding Jalali date and time.

        Example:
        >>> g_date = datetime(2021, 3, 21, 15, 30, 45)
        >>> j_date = JalaliDateTime.to_jalali(g_date)
        >>> print(j_date)
        JalaliDateTime(1400, 1, 1, 15, 30, 45)

        >>> j_date = JalaliDateTime.to_jalali(2021, 3, 21, 15, 30, 45)
        >>> print(j_date)
        JalaliDateTime(1400, 1, 1, 15, 30, 45)
        """
        if month is None and isinstance(year, dt):
            month = year.month
            day = year.day
            hour = year.hour
            minute = year.minute
            second = year.second
            microsecond = year.microsecond
            tzinfo = year.tzinfo
            year = year.year

        j_date = JalaliDate.to_jalali(year, month, day)

        return cls.combine(
            j_date,
            _time(hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=tzinfo),
        )

    def to_gregorian(self):
        """
        Convert a Jalali (Persian) datetime to a Gregorian datetime.

        This method converts the current Jalali (Persian) datetime instance to its
        corresponding Gregorian datetime. It considers both date and time components,
        including year, month, day, hour, minute, second, microsecond, and timezone.

        Returns:
        datetime: A datetime.datetime object representing the corresponding Gregorian datetime.

        Example:
        >>> j_datetime = JalaliDateTime(1400, 1, 1, 15, 30, 45)
        >>> g_datetime = j_datetime.to_gregorian()
        >>> print(g_datetime)
        2021-03-21 15:30:45
        """
        g_date = super().to_gregorian()

        return dt.combine(
            g_date,
            _time(
                hour=self._hour,
                minute=self._minute,
                second=self._second,
                microsecond=self._microsecond,
                tzinfo=self._tzinfo,
            ),
        )

    @classmethod
    def strptime(cls, data_string, fmt, locale="en"):
        if locale not in ["en", "fa"]:
            raise ValueError("locale must be 'en' or 'fa'")

        if locale == "fa":
            data_string = digits.fa_to_en(data_string)

        month_names = MONTH_NAMES_EN[1:] if locale == "en" else MONTH_NAMES_FA[1:]
        month_names_abbr = MONTH_NAMES_ABBR_EN[1:] if locale == "en" else MONTH_NAMES_ABBR_FA[1:]
        weekday_names = WEEKDAY_NAMES_EN if locale == "en" else WEEKDAY_NAMES_FA
        weekday_names_abbr = WEEKDAY_NAMES_ABBR_EN if locale == "en" else WEEKDAY_NAMES_ABBR_FA
        periods = ["AM", "PM"] if locale == "en" else ["ق.ظ", "ب.ظ"]

        """
        these patterns are derived from python official documentation on strftime and strptime behavior:
        link: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        look for the table under "strftime() and strptime() Format Codes" section.
        """
        directives_regex_pattern = {
            "%Y": r"(?P<Y>\d\d\d\d)",
            "%m": r"(?P<m>1[0-2]|0[1-9]|[1-9])",
            "%d": r"(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])",
            "%a": cls.__seqToRE(cls, weekday_names_abbr, "a"),
            "%A": cls.__seqToRE(cls, weekday_names, "A"),
            "%b": cls.__seqToRE(cls, month_names_abbr, "b"),
            "%B": cls.__seqToRE(cls, month_names, "B"),
            "%H": r"(?P<H>2[0-3]|[0-1]\d|\d)",
            "%I": r"(?P<I>1[0-2]|0[1-9]|[1-9])",
            "%p": cls.__seqToRE(cls, periods, "p"),
            "%M": r"(?P<M>[0-5]\d|\d)",
            "%S": r"(?P<S>6[0-1]|[0-5]\d|\d)",
            "%f": r"(?P<f>\d{1,6})",
            "%z": r"(?P<z>[-+](?P<zH>[0-1]?[0-9]|2[0-3])(?P<zM>[0-5]?[0-9])(?P<zS>[0-5]?[0-9])?(\.(?P<zf>(\d{,6})))?)",
            "%Z": cls.__seqToRE(cls, pytz.all_timezones, "Z"),
        }

        fmt = utils.replace(
            fmt,
            {
                "%c": "%A %d %B %Y %H:%M:%S",
                "%x": "%Y/%m/%d",
                "%X": "%H:%M:%S",
            },
        )

        data_string_regex = utils.replace(fmt, directives_regex_pattern)

        if re.match(data_string_regex, data_string, re.IGNORECASE):
            directives = re.search(data_string_regex, data_string, re.IGNORECASE).groupdict()

            if "Y" in directives.keys() and len(directives.get("Y")) < 4:
                raise ValueError("Year element must contain exactly 4 digits")

            directives = {k: int(v) if v.isdigit() else v for k, v in directives.items() if v}

            # extraction of month number from %b|%B format
            if ("b" in directives.keys() or "B" in directives.keys()) and "m" not in directives.keys():
                name, is_abbr = (
                    (directives.pop("b"), True) if "b" in directives.keys() else (directives.pop("B"), False)
                )
                directives["m"] = (month_names_abbr.index(name) if is_abbr else month_names.index(name)) + 1

            # extraction of hour from periodic time format
            if "p" in directives.keys():
                if "I" in directives.keys():
                    directives["H"] = directives.pop("I") + (0 if directives["p"].upper() == periods[0] else 12)
                else:
                    raise ValueError("using %p requires to use %I (12 hour format) as well")

            # extraction of timezone information if provided
            tz = None
            if "z" in directives.keys():
                sign = 1 if directives["z"][0] == "+" else -1
                delta = timedelta(
                    hours=sign * directives["zH"],
                    minutes=sign * directives["zM"],
                    seconds=sign * directives.get("zS", 0),
                    microseconds=sign * directives.get("zf", 0),
                )
                tz = timezone(delta)
            elif "Z" in directives.keys():
                tz = pytz.timezone(directives.get("Z"))

            cls_attrs = {
                "year": directives.get("Y", 1),
                "month": directives.get("m", 1),
                "day": directives.get("d", 1),
                "hour": directives.get("H", 0),
                "minute": directives.get("M", 0),
                "second": directives.get("S", 0),
                "microsecond": directives.get("f", 0),
                "tzinfo": tz,
                "locale": locale,
            }

            return cls(**cls_attrs)
        else:
            raise ValueError("data string and format are not matched")

    def __seqToRE(self, to_convert, directive):
        to_convert = sorted(to_convert, key=len, reverse=True)
        for value in to_convert:
            if value != "":
                break
        else:
            return ""
        regex = "|".join(re_escape(stuff) for stuff in to_convert)
        regex = f"(?P<{directive}>{regex}"
        return "%s)" % regex

    def __repr__(self):
        """Convert to formal string, for repr()."""
        d_datetime = [
            self._year,
            self._month,
            self._day,  # These are never zero
            self._hour,
            self._minute,
            self._second,
            self._microsecond,
        ]

        if d_datetime[-1] == 0:
            del d_datetime[-1]

        if d_datetime[-1] == 0:
            del d_datetime[-1]

        s = ", ".join(map(str, d_datetime))
        s = "{}({})".format("JalaliDateTime", s)

        if self._tzinfo is not None:
            assert s[-1:] == ")"
            s = s[:-1] + ", tzinfo=%r" % self._tzinfo + ")"

        return s

    def __str__(self):
        return self.isoformat(sep=" ")

    def strftime(self, fmt: str, locale=None) -> str:
        if locale is None or locale not in ["fa", "en"]:
            locale = self._locale

        datetime = self.to_gregorian()

        format_time = {
            "%H": "%02d" % self._hour,
            "%I": "%02d" % (self._hour if self._hour <= 12 else self._hour - 12),
            "%p": "AM" if self._hour < 12 else "PM",
            "%M": "%02d" % self._minute,
            "%S": "%02d" % self._second,
            "%f": "%06d" % self._microsecond,
            "%z": datetime.strftime("%z"),
            "%Z": ("" if not self._tzinfo else self._tzinfo.tzname(datetime)),
            "%X": "%02d:%02d:%02d" % (self._hour, self._minute, self._second),
        }

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": "%A %d %B %Y %X"})

        result = utils.replace(fmt, format_time)

        result = super().strftime(result, locale)

        return result

    def __base_compare(self, other):
        assert isinstance(other, JalaliDateTime)

        y, mo, d, h, m, s, ms = [
            self._year,
            self._month,
            self._day,
            self._hour,
            self._minute,
            self._second,
            self._microsecond,
        ]
        y2, mo2, d2, h2, m2, s2, ms2 = [
            other.year,
            other.month,
            other.day,
            other.hour,
            other.minute,
            other.second,
            other.microsecond,
        ]

        return (
            0
            if (y, mo, d, h, m, s, ms) == (y2, mo2, d2, h2, m2, s2, ms2)
            else 1 if (y, mo, d, h, m, s, ms) > (y2, mo2, d2, h2, m2, s2, ms2) else -1
        )

    def _cmp(self, other, allow_mixed=False):
        """
        Compare the current JalaliDateTime object with another JalaliDateTime object.

        This method compares two JalaliDateTime objects, taking into account their
        timezone offsets. It returns:
        - 0 if both objects represent the same point in time.
        - 1 if the current object is later than the other.
        - -1 if the current object is earlier than the other.

        Parameters:
        other (JalaliDateTime): The other JalaliDateTime object to compare with.
        allow_mixed (bool, optional): If True, allows comparison between naive and aware datetimes,
                                    returning an arbitrary non-zero value. Defaults to False.

        Returns:
        int: 0 if both objects represent the same time, 1 if the current object is later,
            -1 if the current object is earlier.

        Raises:
        TypeError: If trying to compare naive and aware datetimes when allow_mixed is False.

        Example:
        >>> jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        >>> jdt2 = JalaliDateTime(1400, 1, 1, 13, 30, 45, tzinfo=timezone.utc)
        >>> jdt1._cmp(jdt2)
        -1
        >>> jdt2._cmp(jdt1)
        1
        >>> jdt1._cmp(jdt1)
        0
        """
        assert isinstance(other, JalaliDateTime)

        mytz = self._tzinfo
        ottz = other.tzinfo
        myoff = otoff = None

        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            base_compare = myoff == otoff

        if base_compare:
            return self.__base_compare(other)

        if myoff is None or otoff is None:
            if allow_mixed:
                return 2  # arbitrary non-zero value
            raise TypeError("cannot compare naive and aware datetimes")

        diff = self - other  # this will take offsets into account
        if diff.days < 0:
            return -1

        return diff and 1 or 0

    def __eq__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other, allow_mixed=True) == 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other), allow_mixed=True) == 0

        return False

    def __ne__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other, allow_mixed=True) != 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other), allow_mixed=True) != 0

        return True

    def __le__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) <= 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) <= 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(f"can't compare '{type(self).__name__}' to '{type(other).__name__}'")

    def __lt__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) < 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) < 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(f"can't compare '{type(self).__name__}' to '{type(other).__name__}'")

    def __ge__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) >= 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) >= 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(f"can't compare '{type(self).__name__}' to '{type(other).__name__}'")

    def __gt__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) > 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) > 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(f"can't compare '{type(self).__name__}' to '{type(other).__name__}'")

    def __add__(self, other):
        if not isinstance(other, timedelta):
            raise NotImplementedError

        delta = timedelta(
            self.toordinal(),
            hours=self._hour,
            minutes=self._minute,
            seconds=self._second,
            microseconds=self._microsecond,
        )
        delta += other
        hour, rem = divmod(delta.seconds, 3600)
        minute, second = divmod(rem, 60)

        if 0 < delta.days <= _MAXORDINAL:
            return JalaliDateTime.combine(
                JalaliDate.fromordinal(delta.days),
                _time(hour, minute, second, delta.microseconds, tzinfo=self._tzinfo),
            )

        raise OverflowError("result out of range")

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, dt):
            other = JalaliDateTime(other)

        if not isinstance(other, JalaliDateTime):
            if isinstance(other, timedelta):
                return self + -other
            raise NotImplementedError

        days1 = self.toordinal()
        days2 = other.toordinal()
        secs1 = self._second + self._minute * 60 + self._hour * 3600
        secs2 = other.second + other.minute * 60 + other.hour * 3600
        base = timedelta(days1 - days2, secs1 - secs2, self._microsecond - other.microsecond)

        if self._tzinfo is other.tzinfo:
            return base

        myoff = self.utcoffset()
        otoff = other.utcoffset()
        if myoff == otoff:
            return base

        if myoff is None or otoff is None:
            raise TypeError("cannot mix naive and timezone-aware time")

        return base + otoff - myoff

    def __hash__(self):
        tzoff = self.utcoffset()

        if tzoff is None:
            return hash(self.__getstate__()[0])

        days = self.toordinal()
        seconds = self.hour * 3600 + self.minute * 60 + self.second
        return hash(timedelta(days, seconds, self.microsecond) - tzoff)

    def __getstate__(self):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        basestate = bytes(
            [
                yhi,
                ylo,
                self._month,
                self._day,
                self._hour,
                self._minute,
                self._second,
                us1,
                us2,
                us3,
            ]
        )
        if self._tzinfo is None:
            return (basestate,)

        return basestate, self._tzinfo

    def __setstate__(self, string, tzinfo):
        (
            yhi,
            ylo,
            self._month,
            self._day,
            self._hour,
            self._minute,
            self._second,
            us1,
            us2,
            us3,
        ) = string

        self._year = yhi * 256 + ylo
        self._microsecond = (((us1 << 8) | us2) << 8) | us3

        if tzinfo is None or isinstance(tzinfo, _tzinfo_class):
            self._tzinfo = tzinfo
        else:
            raise TypeError("bad tzinfo state arg %r" % tzinfo)

    def __reduce__(self):
        return self.__class__, self.__getstate__()
