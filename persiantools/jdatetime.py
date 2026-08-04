import operator
import re
import warnings
from bisect import bisect_left
from collections import namedtuple
from datetime import date
from datetime import datetime as dt
from datetime import time as _time
from datetime import timedelta, timezone, tzinfo
from re import escape as re_escape
from typing import ClassVar
from zoneinfo import ZoneInfo

from persiantools import digits, utils

MINYEAR = 1
MAXYEAR = 9377
_MAXORDINAL = 3424878

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

WEEKDAY_NAMES_EN = [
    "Shanbeh",
    "Yekshanbeh",
    "Doshanbeh",
    "Seshanbeh",
    "Chaharshanbeh",
    "Panjshanbeh",
    "Jomeh",
]

WEEKDAY_NAMES_FA = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

WEEKDAY_NAMES_ABBR_EN = ["Sha", "Yek", "Dos", "Ses", "Cha", "Pan", "Jom"]

WEEKDAY_NAMES_ABBR_FA = ["ش", "ی", "د", "س", "چ", "پ", "ج"]

# Columns: [common-year days, leap-year days, days before month in a common year].
# Index 0 is unused so months are 1-indexed.
_MONTH_COUNT = [
    [-1, -1, -1],
    [31, 31, 0],
    [31, 31, 31],
    [31, 31, 62],
    [31, 31, 93],
    [31, 31, 124],
    [31, 31, 155],
    [30, 30, 186],
    [30, 30, 216],
    [30, 30, 246],
    [30, 30, 276],
    [30, 30, 306],
    [29, 30, 336],
]

_FRACTION_CORRECTION = [100000, 10000, 1000, 100, 10]

_MONTH_DAYS = tuple(row[0] for row in _MONTH_COUNT)
_MONTH_DAYS_LEAP = tuple(row[1] for row in _MONTH_COUNT)
_DAYS_BEFORE_MONTH = tuple(row[2] for row in _MONTH_COUNT)

_LOCALES = ("en", "fa")

_STRFTIME_DIRECTIVE_RE = re.compile(r"%(:z|.)")

# Years that are exceptions to the 33-year leap year rule.
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

# Proleptic Gregorian ordinal of the day before 1 Farvardin 1, so that Jalali
# ordinals start at 1 like date.toordinal(). The epoch of the Solar Hijri
# calendar is Friday 1 Farvardin 1 = 19 March 622 Julian = 22 March 622
# proleptic Gregorian (R.D. 226896), following the standard astronomical
# definition (Calendrical Calculations; the same epoch used by the official
# Iranian calendar authority's model).
_EPOCH_ORDINAL = 226895

# Number of leap years among the first `phase` years of a 33-year cycle under
# the (25 * year + 11) % 33 < 8 rule used by is_leap; entry `phase` covers
# years 33 * cycles + 1 through 33 * cycles + phase.
# fmt: off
_LEAPS_BEFORE_CYCLE_YEAR = (
    0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
    5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8,
)
# fmt: on

# Last year of the ancient regime, where leap years follow the astronomical
# calendar (vernal equinox at the 52.5 E meridian) instead of the plain
# 33-year rule.
_ANCIENT_MAX = 1177

# Years 1..1177 whose leap status under the astronomical calendar differs
# from the (25 * year + 11) % 33 < 8 rule. Data derived from
# https://github.com/roozbehp/persiancalendar (Apache 2.0), the Calendrical
# Calculations astronomical Persian calendar at the 52.5 E meridian, which
# reproduces the official leap-year table of the Iranian calendar authority
# (Calendar Center, Institute of Geophysics, University of Tehran) exactly.
# Five astronomical flip pairs -- (978, 979), (1011, 1012), (1044, 1045),
# (1077, 1078), (1176, 1177) -- are excluded: their effects would reach into
# Gregorian 1601+, where all established implementations agree with the
# 33-year rule, and each hinges on an equinox missing the midday cutoff by
# mere minutes (36 s .. 11 min), far inside ephemeris model uncertainty.
# From year 1178 on both models coincide, so this table is complete, and
# conversions are unchanged for every day on or after Gregorian 1568-03-21.
# fmt: off
_ANCIENT_LEAP_FLIPS = (
    1, 21, 22, 25, 26, 29, 30, 33, 34, 54, 55, 58, 59, 62, 63, 66, 67, 87, 88, 91, 92, 95, 96, 99, 100, 120, 121,
    124, 125, 128, 129, 132, 133, 153, 154, 157, 158, 161, 162, 186, 187, 190, 191, 194, 195, 219, 220, 223, 224,
    227, 228, 252, 253, 256, 257, 260, 261, 285, 286, 289, 290, 293, 294, 318, 319, 322, 323, 326, 327, 351, 352,
    355, 356, 359, 360, 384, 385, 388, 389, 392, 393, 417, 418, 421, 422, 450, 451, 454, 455, 483, 484, 487, 488,
    516, 517, 520, 521, 549, 550, 553, 554, 582, 583, 586, 587, 615, 616, 619, 620, 648, 649, 652, 653, 681, 682,
    714, 715, 747, 748, 780, 781, 784, 785, 813, 814, 846, 847, 879, 880, 912, 913, 945, 946,
)
# fmt: on

_ANCIENT_LEAP_FLIPS_SET = frozenset(_ANCIENT_LEAP_FLIPS)

# Split of the flips by direction, for cumulative-day corrections: "on" years
# are leap only astronomically, "off" years only under the 33-year rule. The
# off years outnumber the on years by exactly one, which cancels the epoch
# falling one day after the arithmetic model's epoch, so both models place
# every Norouz from 1178 on the same Gregorian day.
_ANCIENT_FLIPS_ON = tuple(y for y in _ANCIENT_LEAP_FLIPS if (25 * y + 11) % 33 >= 8)
_ANCIENT_FLIPS_OFF = tuple(y for y in _ANCIENT_LEAP_FLIPS if (25 * y + 11) % 33 < 8)


def _days_before_year(year: int) -> int:
    """Number of days from the Jalali epoch to 1 Farvardin of `year`.

    Kept exactly consistent with is_leap: each full 33-year cycle contributes
    8 leap days, each ancient flip year shifts the start of every later year
    by one day, and each correction year (never leap, but always followed by
    a leap successor) only shifts its successor's start one day earlier.
    """
    cycles, phase = divmod(year - 1, 33)
    days = 365 * (year - 1) + 8 * cycles + _LEAPS_BEFORE_CYCLE_YEAR[phase]

    if year > _ANCIENT_MAX:
        days -= 1
        # Correction years are all >= 1502, so this lookup is only needed here.
        if (year - 1) in NON_LEAP_CORRECTION_SET:
            days -= 1
    else:
        days += bisect_left(_ANCIENT_FLIPS_ON, year) - bisect_left(_ANCIENT_FLIPS_OFF, year)

    return days


def _is_ascii_digit(c: str) -> bool:
    return c in "0123456789"


def _jalali_from_days(days: int):
    """Jalali (year, month, day) fields from days since the Jalali epoch (1 Farvardin 1 = day 1)."""
    # First approximation from the cycle's mean year length (12053 days
    # per 33 years), then settle on the year whose span contains the day.
    # The estimate is off by at most a year or two, so each loop below
    # runs O(1) times.
    days_before_year = _days_before_year
    jalali_year = days * 33 // 12053 + 1
    while days <= days_before_year(jalali_year):
        jalali_year -= 1
    while days > days_before_year(jalali_year + 1):
        jalali_year += 1

    day_of_year = days - days_before_year(jalali_year)

    # The first 6 Jalali months have 31 days, the remaining 6 have 30.
    if day_of_year <= 186:
        jalali_month = 1 + (day_of_year - 1) // 31
        jalali_day = 1 + (day_of_year - 1) % 31
    else:
        jalali_month = 7 + (day_of_year - 187) // 30
        jalali_day = 1 + (day_of_year - 187) % 30

    return jalali_year, jalali_month, jalali_day


# Mirrors datetime.date.isocalendar() result type.
IsoCalendarDate = namedtuple("IsoCalendarDate", ["year", "week", "weekday"])


class JalaliDate:
    """
    Represents a date in the Jalali (Persian) calendar.

    Attributes:
        year (int): The year of the Jalali date.
        month (int): The month of the Jalali date.
        day (int): The day of the Jalali date.
        locale (str): The locale for the Jalali date ('en' or 'fa').
    """

    __slots__ = "_year", "_month", "_day", "_locale", "_hashcode"

    min: ClassVar["JalaliDate"]
    max: ClassVar["JalaliDate"]

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
        if locale not in _LOCALES:
            raise ValueError("locale must be 'en' or 'fa'")

        if isinstance(year, JalaliDate) and month is None:
            year, month, day, locale = year.year, year.month, year.day, year.locale

        elif isinstance(year, date):
            year, month, day = _jalali_from_days(year.toordinal() - _EPOCH_ORDINAL)

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

        if locale not in _LOCALES:
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

        Years 1..1177 follow the astronomical calendar (vernal equinox at the
        52.5 E meridian, per Calendrical Calculations and the model used by the
        official Iranian calendar authority), encoded as flips against the
        33-year rule. Years 1502..2987 apply the correction set from the ICU4X
        project:
        https://github.com/unicode-org/icu4x/blob/main/utils/calendrical_calculations/src/persian.rs

        Args:
            year (int): The Persian year to check.

        Returns:
            bool: True if the year is a leap year, False otherwise.
        """
        if not (MINYEAR <= year <= MAXYEAR):
            raise ValueError(f"Year must be between {MINYEAR} and {MAXYEAR}")

        if year > _ANCIENT_MAX:
            if year >= MIN_NON_LEAP_CORRECTION:
                if year in NON_LEAP_CORRECTION_SET:
                    return False

                if (year - 1) in NON_LEAP_CORRECTION_SET:
                    return True

            return (25 * year + 11) % 33 < 8

        return ((25 * year + 11) % 33 < 8) != (year in _ANCIENT_LEAP_FLIPS_SET)

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
            return _MONTH_DAYS_LEAP[12]

        return _MONTH_DAYS[month]

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

        return _DAYS_BEFORE_MONTH[month]

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
            year, month, day = year.year, year.month, year.day

        return cls._from_days(date(year, month, day).toordinal() - _EPOCH_ORDINAL)

    @classmethod
    def _from_days(cls, days: int):
        """Build an instance from days since the Jalali epoch (1 Farvardin 1 = day 1)."""
        jalali_year, jalali_month, jalali_day = _jalali_from_days(days)

        if cls is JalaliDate and MINYEAR <= jalali_year <= MAXYEAR:
            # Fast path: the computed fields are known to be valid, so the
            # instance can be populated without re-validating in __init__.
            self = object.__new__(cls)
            self._year = jalali_year
            self._month = jalali_month
            self._day = jalali_day
            self._locale = "en"
            self._hashcode = -1
            return self

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
        return date.fromordinal(_EPOCH_ORDINAL + self.toordinal())

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
        return _days_before_year(self._year) + _DAYS_BEFORE_MONTH[self._month] + self._day

    @classmethod
    def fromordinal(cls, n: int):
        return cls._from_days(n)

    @classmethod
    def fromisocalendar(cls, year, week, day):
        """
        Construct a JalaliDate from the ISO-like calendar used by `isocalendar()`.

        This is the inverse of `isocalendar()`: given a Jalali year, a week number
        (as returned by `week_of_year()`) and a weekday (1 = Shanbeh .. 7 = Jomeh,
        as returned by `isoweekday()`), return the corresponding date.

        Args:
            year (int): The Jalali year.
            week (int): The week of the year, as returned by `week_of_year()`.
            day (int): The weekday, 1 (Shanbeh) through 7 (Jomeh).

        Returns:
            JalaliDate: The date identified by (year, week, day).

        Raises:
            ValueError: If year, week, or day do not identify a valid date of that year.
        """
        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError(f"Year is out of range: {year}")

        if not 1 <= week <= 53:
            raise ValueError(f"Invalid week: {week}")

        if not 1 <= day <= 7:
            raise ValueError(f"Invalid weekday: {day} (range is [1, 7])")

        first_day = JalaliDate(year, 1, 1)
        ordinal = first_day.toordinal() + (week - 1) * 7 + (day - 1) - first_day.weekday()

        if not 0 < ordinal <= _MAXORDINAL:
            raise ValueError(f"Invalid week: {week}")

        result = cls.fromordinal(ordinal)
        if result.isocalendar() != (year, week, day):
            raise ValueError(f"Invalid week: {week}")

        return result

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
        # Port of CPython's `_parse_isoformat_date` (Python 3.11+), adapted to
        # the Jalali calendar. Accepts YYYY-MM-DD, YYYYMMDD and the week-date
        # forms YYYY-Www[-D] / YYYYWww[d]. ASCII-only input is assumed.
        if len(dtstr) < 7 or not dtstr[0:4].isdigit():
            raise ValueError("Invalid ISO string")

        year = int(dtstr[0:4])
        has_sep = dtstr[4] == "-"

        pos = 4 + has_sep
        if dtstr[pos : pos + 1] == "W":
            # YYYY-?Www-?D?
            pos += 1
            weekno = int(dtstr[pos : pos + 2])
            pos += 2

            dayno = 1
            if len(dtstr) > pos:
                if (dtstr[pos : pos + 1] == "-") != has_sep:
                    raise ValueError("Inconsistent use of dash separator")

                pos += has_sep

                dayno = int(dtstr[pos : pos + 1])
                pos += 1

            if pos != len(dtstr):
                raise ValueError("Invalid ISO string")

            result = JalaliDate.fromisocalendar(year, weekno, dayno)
            return [result.year, result.month, result.day]
        else:
            month = int(dtstr[pos : pos + 2])
            pos += 2

            if (dtstr[pos : pos + 1] == "-") != has_sep:
                raise ValueError("Inconsistent use of dash separator")

            pos += has_sep
            day = int(dtstr[pos : pos + 2])

            if pos + 2 != len(dtstr):
                raise ValueError("Invalid ISO string")

            cls._check_date_fields(year, month, day, "en")

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

    def __replace__(self, **changes):
        """Support for copy.replace() (Python 3.13+)."""
        return self.replace(**changes)

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
        return (self.toordinal() + 5) % 7

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
        # Weekday of 1 Farvardin of this year, inlined from
        # JalaliDate(self._year, 1, 1).weekday() to avoid building an instance.
        o = (_days_before_year(self._year) + 6) % 7
        days = _DAYS_BEFORE_MONTH[self._month] + self._day + o

        week_no, r = divmod(days, 7)

        if r > 0:
            week_no += 1

        return week_no

    def isocalendar(self):
        """
        Return a named tuple containing ISO year, week number, and weekday.

        Returns:
            IsoCalendarDate: A named tuple (year, week, weekday); compares equal
            to the plain 3-tuple returned by earlier versions.
        """
        return IsoCalendarDate(self.year, self.week_of_year(), self.isoweekday())

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
        if locale is None or locale not in _LOCALES:
            locale = self._locale

        if locale == "en":
            month_names = MONTH_NAMES_EN
            month_names_abbr = MONTH_NAMES_ABBR_EN
            day_names = WEEKDAY_NAMES_EN
            day_names_abbr = WEEKDAY_NAMES_ABBR_EN
            am = "AM"
        else:
            month_names = MONTH_NAMES_FA
            month_names_abbr = MONTH_NAMES_ABBR_FA
            day_names = WEEKDAY_NAMES_FA
            day_names_abbr = WEEKDAY_NAMES_ABBR_FA
            am = "ق.ظ"

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": "%A %d %B %Y"})

        if "%x" in fmt:
            fmt = utils.replace(fmt, {"%x": "%y/%m/%d"})

        # Single-pass substitution with lazily computed values: only the
        # directives actually present in the format string are evaluated,
        # and repeated directives share the computed value.
        values: dict[str, str] = {}
        weekday = -1
        week_of_year = -1

        def _replace_directive(match):
            nonlocal weekday, week_of_year

            code = match.group(1)
            value = values.get(code)
            if value is not None:
                return value

            if code == "d":
                value = "%02d" % self._day
            elif code == "m":
                value = "%02d" % self._month
            elif code == "y":
                value = "%02d" % (self._year % 100)
            elif code == "Y":
                value = "%04d" % self._year
            elif code == "b":
                value = month_names_abbr[self._month]
            elif code == "B":
                value = month_names[self._month]
            elif code == "a" or code == "A" or code == "w":
                if weekday < 0:
                    weekday = self.weekday()

                if code == "a":
                    value = day_names_abbr[weekday]
                elif code == "A":
                    value = day_names[weekday]
                else:
                    value = str(weekday)
            elif code == "j":
                value = "%03d" % (_DAYS_BEFORE_MONTH[self._month] + self._day)
            elif code == "U" or code == "W":
                if week_of_year < 0:
                    week_of_year = self.week_of_year()

                value = "%02d" % week_of_year
            elif code == "H" or code == "I" or code == "M" or code == "S":
                value = "00"
            elif code == "p":
                value = am
            elif code == "f":
                value = "000000"
            elif code == ":z" or code == "z" or code == "Z":
                value = ""
            elif code == "X":
                value = "00:00:00"
            elif code == "%":
                value = "%"
            else:
                return match.group(0)

            values[code] = value
            return value

        result = _STRFTIME_DIRECTIVE_RE.sub(_replace_directive, fmt)

        if locale == "fa":
            result = digits.en_to_fa(result)

        return result

    def _compare(self, other):
        assert isinstance(other, JalaliDate)

        t1 = (self._year, self._month, self._day)
        t2 = (other._year, other._month, other._day)

        return (t1 > t2) - (t1 < t2)

    def _compare_date(self, other):
        """Compare with a datetime.date (or datetime) operand without building a JalaliDate."""
        t1 = (self._year, self._month, self._day)
        t2 = _jalali_from_days(other.toordinal() - _EPOCH_ORDINAL)

        return (t1 > t2) - (t1 < t2)

    def __eq__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) == 0
        elif isinstance(other, date):
            return self._compare_date(other) == 0

        return False

    def __ne__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) != 0
        elif isinstance(other, date):
            return self._compare_date(other) != 0

        return True

    def __le__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) <= 0
        elif isinstance(other, date):
            return self._compare_date(other) <= 0

        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) < 0
        elif isinstance(other, date):
            return self._compare_date(other) < 0

        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) >= 0
        elif isinstance(other, date):
            return self._compare_date(other) >= 0

        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) > 0
        elif isinstance(other, date):
            return self._compare_date(other) > 0

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
            y, m, d = _jalali_from_days(other.toordinal() - _EPOCH_ORDINAL)
            days2 = _days_before_year(y) + _DAYS_BEFORE_MONTH[m] + d

            return timedelta(days1 - days2)

        raise NotImplementedError

    @classmethod
    def strptime(cls, data_string, fmt, locale="en"):
        if locale not in _LOCALES:
            raise ValueError("locale must be 'en' or 'fa'")

        if locale == "fa":
            data_string = digits.fa_to_en(data_string)

        month_names_list = MONTH_NAMES_EN[1:] if locale == "en" else MONTH_NAMES_FA[1:]
        month_names_abbr_list = MONTH_NAMES_ABBR_EN[1:] if locale == "en" else MONTH_NAMES_ABBR_FA[1:]
        weekday_names_list = WEEKDAY_NAMES_EN if locale == "en" else WEEKDAY_NAMES_FA
        weekday_names_abbr_list = WEEKDAY_NAMES_ABBR_EN if locale == "en" else WEEKDAY_NAMES_ABBR_FA

        directives_regex_pattern = {
            "%Y": r"(?P<Y>\d{4})",
            "%y": r"(?P<y>\d{2})",
            "%m": r"(?P<m>1[0-2]|0?[1-9])",
            "%d": r"(?P<d>\d{1,2})",
            "%j": r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            "%w": r"(?P<w>[0-6])",
            "%U": r"(?P<U>5[0-3]|[0-4]\d|\d)",
            "%W": r"(?P<W>5[0-3]|[0-4]\d|\d)",
            "%b": cls._seqToRE(month_names_abbr_list, "b"),
            "%B": cls._seqToRE(month_names_list, "B"),
            "%a": cls._seqToRE(weekday_names_abbr_list, "a"),
            "%A": cls._seqToRE(weekday_names_list, "A"),
        }

        fmt = utils.replace(
            fmt,
            {
                "%x": "%Y/%m/%d",
                "%c": "%a %b %d %Y",
            },
        )

        data_string_regex = utils.replace(fmt, directives_regex_pattern)
        full_pattern = f"^{data_string_regex}$"

        match = re.match(full_pattern, data_string, re.IGNORECASE)
        if not match:
            raise ValueError(f"Date string '{data_string}' does not match format '{fmt}'")

        directives = match.groupdict()

        parsed_components = {}
        for k, v in directives.items():
            if v is not None:
                if k not in ["a", "A", "b", "B"] and v.isdigit():
                    parsed_components[k] = int(v)
                else:
                    parsed_components[k] = v

        year = parsed_components.get("Y")
        yy = parsed_components.get("y")

        if year is None and yy is not None:
            # Heuristic: yy > 70 => 13yy, else 14yy (current era is ~140x).
            year = (1300 + yy) if yy > (2070 - 2000) else (1400 + yy)
        elif year is None:
            raise ValueError("Year information is missing from the date string or format.")

        month = parsed_components.get("m")
        month_name_abbr = parsed_components.get("b")
        month_name_full = parsed_components.get("B")

        if month is None and month_name_abbr is not None:
            normalized_month_abbr = month_name_abbr.capitalize() if locale == "en" else month_name_abbr
            month = month_names_abbr_list.index(normalized_month_abbr) + 1
        elif month is None and month_name_full is not None:
            normalized_month_full = month_name_full.capitalize() if locale == "en" else month_name_full
            month = month_names_list.index(normalized_month_full) + 1

        day = parsed_components.get("d")

        # Derive the date from %j, or from %U/%W combined with %w, mirroring
        # CPython's strptime: an explicit or derived day of year takes
        # precedence over parsed month/day values.
        day_of_year = parsed_components.get("j")
        week_of_year = parsed_components.get("U", parsed_components.get("W"))
        weekday_num = parsed_components.get("w")

        if day_of_year is None and week_of_year is not None and weekday_num is not None:
            day_of_year = (week_of_year - 1) * 7 + weekday_num + 1 - JalaliDate(year, 1, 1).weekday()

        if day_of_year is not None:
            days_in_year = 366 if cls.is_leap(year) else 365
            if not 1 <= day_of_year <= days_in_year:
                raise ValueError(f"Day of year {day_of_year} is out of range for year {year}")

            month = 1
            while day_of_year > cls.days_in_month(month, year):
                day_of_year -= cls.days_in_month(month, year)
                month += 1
            day = day_of_year

        if month is None:
            raise ValueError("Month information is missing from the date string or format.")

        if day is None:
            raise ValueError("Day information is missing from the date string or format.")

        cls._check_date_fields(year, month, day, locale)

        return cls(year, month, day, locale=locale)

    @staticmethod
    def _seqToRE(to_convert, directive):
        to_convert = sorted(to_convert, key=len, reverse=True)
        regex = "|".join(re_escape(stuff) for stuff in to_convert)
        return f"(?P<{directive}>{regex})"


JalaliDate.min = JalaliDate(MINYEAR, 1, 1)
JalaliDate.max = JalaliDate(MAXYEAR, 12, JalaliDate.days_in_month(12, MAXYEAR))

_tzinfo_class = tzinfo


class JalaliDateTime(JalaliDate):
    __slots__ = JalaliDate.__slots__ + ("_hour", "_minute", "_second", "_microsecond", "_tzinfo", "_fold")

    min: ClassVar["JalaliDateTime"]
    max: ClassVar["JalaliDateTime"]

    resolution = timedelta(microseconds=1)

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
        *,
        fold=0,
    ):
        if isinstance(year, JalaliDateTime) and month is None:
            month = year.month
            day = year.day
            hour = year.hour
            minute = year.minute
            second = year.second
            microsecond = year.microsecond
            if tzinfo is None:
                tzinfo = year.tzinfo
            fold = year.fold
            year = year.year

        elif isinstance(year, dt) and month is None:
            j_year, month, day = _jalali_from_days(year.toordinal() - _EPOCH_ORDINAL)
            hour = year.hour
            minute = year.minute
            second = year.second
            microsecond = year.microsecond

            if tzinfo is None:
                tzinfo = year.tzinfo

            fold = year.fold
            year = j_year

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
            fold = self._fold

        super().__init__(year, month, day, locale)
        self._check_tzinfo_arg(tzinfo)
        self._check_time_fields(hour, minute, second, microsecond, fold)

        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._fold = fold

    @staticmethod
    def _check_time_fields(hour, minute, second, microsecond, fold=0):
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

        if fold not in (0, 1):
            raise ValueError("fold must be either 0 or 1", fold)

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

    @property
    def fold(self) -> int:
        """
        Returns the fold attribute (PEP 495), used to disambiguate wall times
        that occur twice, e.g. during a daylight saving time transition.

        Returns:
            int: 0 or 1.
        """
        return self._fold

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        return cls(dt.fromtimestamp(t, tz))

    @classmethod
    def utcfromtimestamp(cls, t):
        warnings.warn(
            "JalaliDateTime.utcfromtimestamp() is deprecated and scheduled for removal in a future version. "
            "Use timezone-aware objects to represent datetimes in UTC: JalaliDateTime.fromtimestamp(t, tz=timezone.utc).",
            DeprecationWarning,
            stacklevel=2,
        )
        return cls(dt.fromtimestamp(t, tz=timezone.utc))

    def date(self):
        return JalaliDate(self.year, self.month, self.day).to_gregorian()

    def jalali_date(self):
        return JalaliDate(self.year, self.month, self.day)

    def jdate(self):
        return self.jalali_date()

    def time(self):
        return _time(self.hour, self.minute, self.second, self.microsecond, fold=self.fold)

    def timetz(self):
        return _time(self.hour, self.minute, self.second, self.microsecond, self.tzinfo, fold=self.fold)

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
        *,
        fold=None,
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

        if fold is None:
            fold = self.fold

        self._check_date_fields(year, month, day, locale)
        self._check_time_fields(hour, minute, second, microsecond, fold)
        self._check_tzinfo_arg(tzinfo)

        return JalaliDateTime(year, month, day, hour, minute, second, microsecond, tzinfo, locale, fold=fold)

    @classmethod
    def now(cls, tz=None):
        return cls(dt.now(tz))

    @classmethod
    def today(cls):
        return cls.now()

    @classmethod
    def utcnow(cls):
        warnings.warn(
            "JalaliDateTime.utcnow() is deprecated and scheduled for removal in a future version. "
            "Use timezone-aware objects to represent datetimes in UTC: JalaliDateTime.now(timezone.utc).",
            DeprecationWarning,
            stacklevel=2,
        )
        return cls(dt.now(tz=timezone.utc))

    @classmethod
    def fromisoformat(cls, date_string: str):
        """Construct a datetime from a string in one of the ISO 8601 formats."""
        if not isinstance(date_string, str):
            raise TypeError("fromisoformat: argument must be str")

        date_string = digits.fa_to_en(date_string)

        if len(date_string) < 7:
            raise ValueError(f"Invalid isoformat string: {date_string!r}")

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
            fold=time_v.fold,
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

    def isoformat(self, sep="T", timespec="auto") -> str:
        s = "%04d-%02d-%02d%c" % (self.year, self.month, self.day, sep) + self._format_time(timespec)

        off = self.utcoffset()
        if off is not None:
            if off.days < 0:
                sign = "-"
                off = -off
            else:
                sign = "+"
            # utcoffset() is validated to be a whole number of minutes
            off_seconds = off.days * 86400 + off.seconds
            hh, mm = divmod(off_seconds, 3600)
            assert not mm % 60, "whole minute"
            mm //= 60
            s += "%s%02d:%02d" % (sign, hh, mm)
        return s

    def _format_time(self, timespec):
        # Mirrors the timespec handling of datetime.datetime.isoformat()
        # (Python 3.6+).
        if timespec == "auto":
            timespec = "microseconds" if self._microsecond else "seconds"

        hour = self._hour
        minute = self._minute
        second = self._second

        if timespec == "hours":
            return "%02d" % hour

        if timespec == "minutes":
            return "%02d:%02d" % (hour, minute)

        if timespec == "seconds":
            return "%02d:%02d:%02d" % (hour, minute, second)

        if timespec == "milliseconds":
            return "%02d:%02d:%02d.%03d" % (hour, minute, second, self._microsecond // 1000)

        if timespec == "microseconds":
            return "%02d:%02d:%02d.%06d" % (hour, minute, second, self._microsecond)

        raise ValueError(f"Unknown timespec value: {timespec!r}")

    def utcoffset(self):
        if self._tzinfo is None:
            return None

        # to_gregorian() always attaches self._tzinfo, so g is aware here
        g = self.to_gregorian()
        try:
            offset = self._tzinfo.utcoffset(g)
        except Exception:
            offset = self._tzinfo.utcoffset(None)

        self.check_utc_offset("utcoffset", offset)
        return offset

    def tzname(self):
        if self._tzinfo is None:
            return None

        g = self.to_gregorian()
        try:
            name = self._tzinfo.tzname(g)
        except Exception:
            name = self._tzinfo.tzname(None)

        if name is not None and not isinstance(name, str):
            raise TypeError("tzinfo.tzname() must return None or string, not '%s'" % type(name))

        return name

    def dst(self):
        """Return DST offset as timedelta or None.

        For stdlib fixed-offset timezones (datetime.timezone, including UTC) this must be timedelta(0).
        """
        if self._tzinfo is None:
            return None

        # datetime.timezone instances (including timezone.utc) never have DST
        if self._tzinfo is timezone.utc or isinstance(self._tzinfo, type(timezone.utc)):
            return timedelta(0)

        g = self.to_gregorian()
        try:
            offset = self._tzinfo.dst(g)
        except Exception:
            offset = self._tzinfo.dst(None)

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
        fold = 0
        if month is None and isinstance(year, dt):
            month = year.month
            day = year.day
            hour = year.hour
            minute = year.minute
            second = year.second
            microsecond = year.microsecond
            tzinfo = year.tzinfo
            fold = year.fold
            year = year.year

        j_date = JalaliDate.to_jalali(year, month, day)

        hour = 0 if hour is None else hour
        minute = 0 if minute is None else minute
        second = 0 if second is None else second
        microsecond = 0 if microsecond is None else microsecond

        return cls.combine(
            j_date,
            _time(hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=tzinfo, fold=fold),
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
                fold=self._fold,
            ),
        )

    @classmethod
    def strptime(cls, data_string, fmt, locale="en"):
        if locale not in _LOCALES:
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
            "%Y": r"(?P<Y>\d{4})",
            "%m": r"(?P<m>1[0-2]|0[1-9]|[1-9])",
            "%d": r"(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])",
            "%j": r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            "%w": r"(?P<w>[0-6])",
            "%U": r"(?P<U>5[0-3]|[0-4]\d|\d)",
            "%W": r"(?P<W>5[0-3]|[0-4]\d|\d)",
            "%a": cls._seqToRE(weekday_names_abbr, "a"),
            "%A": cls._seqToRE(weekday_names, "A"),
            "%b": cls._seqToRE(month_names_abbr, "b"),
            "%B": cls._seqToRE(month_names, "B"),
            "%H": r"(?P<H>2[0-3]|[0-1]\d|\d)",
            "%I": r"(?P<I>1[0-2]|0[1-9]|[1-9])",
            "%p": cls._seqToRE(periods, "p"),
            "%M": r"(?P<M>[0-5]\d|\d)",
            "%S": r"(?P<S>6[0-1]|[0-5]\d|\d)",
            "%f": r"(?P<f>\d{1,6})",
            "%z": (
                r"(?P<z>[-+](?P<zH>2[0-3]|[0-1]\d)"
                r"(?:[:]?)(?P<zM>[0-5]\d)"
                r"(?:[:]?(?P<zS>[0-5]\d))?"
                r"(?:\.(?P<zf>\d{1,6}))?)"
            ),
            "%Z": r"(?P<Z>[A-Za-z_/\-]+)",
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
        full_pattern = f"^{data_string_regex}$"

        if re.match(full_pattern, data_string, re.IGNORECASE):
            directives = re.search(data_string_regex, data_string, re.IGNORECASE).groupdict()

            directives = {k: int(v) if v.isdigit() else v for k, v in directives.items() if v}

            if ("b" in directives.keys() or "B" in directives.keys()) and "m" not in directives.keys():
                name, is_abbr = (
                    (directives.pop("b"), True) if "b" in directives.keys() else (directives.pop("B"), False)
                )
                directives["m"] = (month_names_abbr.index(name) if is_abbr else month_names.index(name)) + 1

            if "p" in directives.keys():
                if "I" in directives.keys():
                    directives["H"] = directives.pop("I") + (0 if directives["p"].upper() == periods[0] else 12)
                else:
                    raise ValueError("using %p requires to use %I (12 hour format) as well")

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
                try:
                    tz = ZoneInfo(directives.get("Z"))
                except Exception:
                    raise ValueError(f"Unknown time zone name: {directives.get('Z')}")

            # derive month/day from %j, or from %U/%W combined with %w,
            # mirroring CPython's strptime precedence
            year = directives.get("Y", 1)
            day_of_year = directives.get("j")
            week_of_year = directives.get("U", directives.get("W"))
            weekday_num = directives.get("w")

            if day_of_year is None and week_of_year is not None and weekday_num is not None:
                day_of_year = (week_of_year - 1) * 7 + weekday_num + 1 - JalaliDate(year, 1, 1).weekday()

            if day_of_year is not None:
                days_in_year = 366 if cls.is_leap(year) else 365
                if not 1 <= day_of_year <= days_in_year:
                    raise ValueError(f"Day of year {day_of_year} is out of range for year {year}")

                month = 1
                while day_of_year > cls.days_in_month(month, year):
                    day_of_year -= cls.days_in_month(month, year)
                    month += 1

                directives["m"] = month
                directives["d"] = day_of_year

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

    def __repr__(self):
        """Convert to formal string, for repr()."""
        d_datetime = [
            self._year,
            self._month,
            self._day,
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

        if self._fold:
            assert s[-1:] == ")"
            s = s[:-1] + ", fold=1)"

        return s

    def __str__(self):
        return self.isoformat(sep=" ")

    def strftime(self, fmt: str, locale=None) -> str:
        if locale is None or locale not in _LOCALES:
            locale = self._locale

        format_time = {
            "%H": "%02d" % self._hour,
            "%I": "%02d" % (self._hour if self._hour <= 12 else self._hour - 12),
            "%p": "AM" if self._hour < 12 else "PM",
            "%M": "%02d" % self._minute,
            "%S": "%02d" % self._second,
            "%f": "%06d" % self._microsecond,
            "%X": "%02d:%02d:%02d" % (self._hour, self._minute, self._second),
        }

        # The Gregorian conversion and the UTC offset are only needed for the
        # timezone directives; compute them lazily.
        if "%:z" in fmt:
            offset = self.utcoffset()
            if offset is None:
                colon_z = ""
            else:
                if offset.days < 0:
                    sign = "-"
                    offset = -offset
                else:
                    sign = "+"
                hh, mm = divmod(offset // timedelta(minutes=1), 60)
                colon_z = "%s%02d:%02d" % (sign, hh, mm)

            format_time["%:z"] = colon_z

        if "%z" in fmt or "%Z" in fmt:
            if self._tzinfo is None:
                # Naive datetimes always format %z and %Z as empty strings.
                if "%z" in fmt:
                    format_time["%z"] = ""

                if "%Z" in fmt:
                    format_time["%Z"] = ""
            else:
                datetime = self.to_gregorian()

                if "%z" in fmt:
                    format_time["%z"] = datetime.strftime("%z")

                if "%Z" in fmt:
                    format_time["%Z"] = self._tzinfo.tzname(datetime)

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": "%A %d %B %Y %X"})

        result = utils.replace(fmt, format_time)

        result = super().strftime(result, locale)

        return result

    def __base_compare(self, other):
        assert isinstance(other, JalaliDateTime)

        t1 = (self._year, self._month, self._day, self._hour, self._minute, self._second, self._microsecond)
        t2 = (
            other._year,
            other._month,
            other._day,
            other._hour,
            other._minute,
            other._second,
            other._microsecond,
        )

        return (t1 > t2) - (t1 < t2)

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
            # Assume that allow_mixed means that we are called from __eq__:
            # an ambiguous wall time (where fold changes the offset) never
            # compares equal across zones (PEP 495).
            if allow_mixed:
                if myoff != self.replace(fold=not self.fold).utcoffset():
                    return 2
                if otoff != other.replace(fold=not other.fold).utcoffset():
                    return 2
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
            # Fast path: the resulting fields are all within their valid
            # ranges, so the instance can be populated directly. As with
            # JalaliDateTime.combine(), the result keeps this instance's
            # tzinfo, uses the default locale, and resets fold to 0.
            year, month, day = _jalali_from_days(delta.days)
            result = object.__new__(JalaliDateTime)
            result._year = year
            result._month = month
            result._day = day
            result._locale = "en"
            result._hashcode = -1
            result._hour = hour
            result._minute = minute
            result._second = second
            result._microsecond = delta.microseconds
            result._tzinfo = self._tzinfo
            result._fold = 0
            return result

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
        t = self.replace(fold=0) if self.fold else self
        tzoff = t.utcoffset()

        if tzoff is None:
            return hash(t.__getstate__()[0])

        days = t.toordinal()
        seconds = t.hour * 3600 + t.minute * 60 + t.second
        return hash(timedelta(days, seconds, t.microsecond) - tzoff)

    def __getstate__(self):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        # fold is encoded in the month byte, as in datetime.datetime (PEP 495)
        month = self._month + 128 * self._fold
        basestate = bytes(
            [
                yhi,
                ylo,
                month,
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
            month,
            self._day,
            self._hour,
            self._minute,
            self._second,
            us1,
            us2,
            us3,
        ) = string

        if month > 127:
            self._fold = 1
            self._month = month - 128
        else:
            self._fold = 0
            self._month = month

        self._year = yhi * 256 + ylo
        self._microsecond = (((us1 << 8) | us2) << 8) | us3

        if tzinfo is None or isinstance(tzinfo, _tzinfo_class):
            self._tzinfo = tzinfo
        else:
            raise TypeError("bad tzinfo state arg %r" % tzinfo)

    def __reduce__(self):
        return self.__class__, self.__getstate__()


JalaliDateTime.min = JalaliDateTime(MINYEAR, 1, 1)
JalaliDateTime.max = JalaliDateTime(MAXYEAR, 12, JalaliDate.days_in_month(12, MAXYEAR), 23, 59, 59, 999999)
