# -*- coding: utf-8 -*-
from datetime import date, timedelta

from persiantools import digits, utils

MINYEAR = 1
MAXYEAR = 9377
_MAXORDINAL = 3424878

MONTH_NAMES_EN = [None, 'Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 'Mehr', 'Aban',
                  'Azar', 'Dey', 'Bahman', 'Esfand']
MONTH_NAMES_FA = [None, 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'یهمن',
                  'اسفند']

MONTH_NAMES_ABBR_EN = [None, 'Far', 'Ord', 'Kho', 'Tir', 'Mor', 'Sha', 'Meh', 'Aba', 'Aza', 'Dey', 'Bah', 'Esf']
MONTH_NAMES_ABBR_FA = [None, 'فرو', 'ارد', 'خرد', 'تیر', 'مرد', 'شهر', 'مهر', 'آبا', 'آذر', 'دی',
                       'بهم', 'اسف']

WEEKDAY_NAMES_EN = ['Shanbeh', 'Yekshanbeh', 'Doshanbeh', 'Seshanbeh', 'Chaharshanbeh', 'Panjshanbeh', 'Jomeh']
WEEKDAY_NAMES_FA = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']

WEEKDAY_NAMES_ABBR_EN = ['Sha', 'Yek', 'Dos', 'Ses', 'Cha', 'Pan', 'Jom']
WEEKDAY_NAMES_ABBR_FA = ['شن', 'یک', 'دو', 'سه', 'چه', 'پن', 'جم']

_MONTH_COUNT = [
    [-1, -1, -1],  # for indexing purposes
    [31, 31, 0],  # farvardin
    [31, 31, 31],  # ordibehesht
    [31, 31, 62],  # khordad
    [31, 31, 93],  # tir
    [31, 31, 124],  # mordad
    [31, 31, 155],  # shahrivar
    [30, 30, 186],  # mehr
    [30, 30, 216],  # aban
    [30, 30, 246],  # azar
    [30, 30, 276],  # dey
    [30, 30, 306],  # bahman
    [29, 30, 336]  # esfand
]


class JalaliDate(object):
    __slots__ = '__year', '__month', '__day', '__locale', '__hashcode'

    def __init__(self, year, month=None, day=None, locale="en"):
        if isinstance(year, JalaliDate):
            month = year.month
            day = year.day
            locale = year.locale
            year = year.year

        elif isinstance(year, date):
            jdate = self.to_jalali(year)
            year, month, day = jdate.year, jdate.month, jdate.day

        elif isinstance(year, str) and month is None and day is None:
            # Pickle support, Python > 2.7
            year = year.strip("[]").split(",")
            if 1 <= int(year[2]) <= 12 and 1 <= int(year[3]) <= 31:
                month = int(year[2])
                day = int(year[3])
                year = int(year[0]) * 256 + int(year[1])

        elif isinstance(year, bytes) and len(year) == 4 and 1 <= year[2] <= 12 and month is None:
            # Pickle support, Python > 3.3
            self.__setstate__(year)
            year = self.__year
            month = self.__month
            day = self.__day

        year, month, day, locale = self.__check_date_fields(year, month, day, locale)

        self.__year = year
        self.__month = month
        self.__day = day
        self.__locale = locale
        self.__hashcode = -1

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    @property
    def locale(self):
        return self.__locale

    @locale.setter
    def locale(self, locale):
        assert locale in ("en", "fa"), "locale must be 'en' or 'fa'"
        self.__locale = locale

    @classmethod
    def __check_date_fields(cls, year, month, day, locale):
        year = utils.check_int_field(year)
        month = utils.check_int_field(month)
        day = utils.check_int_field(day)

        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)

        if not 1 <= month <= 12:
            raise ValueError('month must be in 1..12', month)

        dim = cls.days_in_month(month, year)
        if not 1 <= day <= dim:
            raise ValueError('day must be in 1..%d' % dim, day)

        if locale not in ['en', 'fa']:
            raise ValueError("locale must be 'en' or 'fa'")

        return year, month, day, locale

    @classmethod
    def chack_date(cls, year, month, day):
        try:
            cls.__check_date_fields(year, month, day, "en")
        except (ValueError, TypeError):
            return False
        else:
            return True

    @staticmethod
    def is_leap(year):
        assert MINYEAR <= year <= MAXYEAR

        c = 0.24219858156028368  # 683 / 2820
        # return ((year + 2346) * 683) % 2820 < 683
        return ((year + 2346) * c) % 1 < c

    @classmethod
    def days_in_month(cls, month, year):
        assert 1 <= month <= 12, 'month must be in 1..12'

        if month == 12 and cls.is_leap(year):
            return _MONTH_COUNT[month][1]

        return _MONTH_COUNT[month][0]

    @staticmethod
    def days_before_month(month):
        assert 1 <= month <= 12, 'month must be in 1..12'

        return _MONTH_COUNT[month][2]

    # @staticmethod
    # def days_before_year(year):
    #     assert MINYEAR <= year <= MAXYEAR
    #
    #     c = 365.24219858156028368  # 365 + 683 / 2820
    #     return round((year - 1) * c)

    @classmethod
    def to_jalali(cls, year, month=None, day=None):
        """based on jdf.scr.ir"""
        if month is None and isinstance(year, date):
            month = year.month
            day = year.day
            year = year.year

        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

        jy = 0 if year <= 1600 else 979
        year -= 621 if year <= 1600 else 1600
        year2 = year + 1 if month > 2 else year
        days = (365 * year) + int((year2 + 3) / 4) - int((year2 + 99) / 100) + int((year2 + 399) / 400) - 80 + day + \
               g_d_m[month - 1]
        jy += 33 * int(days / 12053)
        days %= 12053
        jy += 4 * int(days / 1461)
        days %= 1461
        jy += int((days - 1) / 365)

        if days > 365:
            days = (days - 1) % 365

        if days < 186:
            jm = 1 + int(days / 31)
            jd = 1 + (days % 31)
        else:
            arit = days - 186
            jm = 7 + int(arit / 30)
            jd = 1 + (arit % 30)

        return cls(jy, jm, jd)

    def to_gregorian(self):
        month = self.month
        day = self.day
        year = self.year

        gy = 621 if year <= 979 else 1600
        year -= 0 if year <= 979 else 979

        d = (month - 1) * 31 if month < 7 else ((month - 7) * 30) + 186
        days = (365 * year) + (int(year / 33) * 8) + int(((year % 33) + 3) / 4) + 78 + day + d

        gy += 400 * int(days / 146097)
        days %= 146097

        if days > 36524:
            days -= 1
            gy += 100 * int(days / 36524)
            days %= 36524

            if days >= 365:
                days += 1

        gy += 4 * int(days / 1461)
        days %= 1461
        gy += int((days - 1) / 365)

        if days > 365:
            days = (days - 1) % 365

        gd = days + 1

        g_d_m = [0, 31, 29 if (gy % 4 == 0 and gy % 100 != 0) or gy % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31,
                 30, 31]
        gm = 0

        for gm, g in enumerate(g_d_m):
            if gd <= g:
                break
            gd -= g

        return date(gy, gm, gd)

    @classmethod
    def today(cls):
        return cls(date.today())

    def timetuple(self):
        raise NotImplemented

    def isoformat(self):
        iso = "%04d-%02d-%02d" % (self.__year, self.__month, self.__day)

        if self.__locale == "fa":
            iso = digits.en_to_fa(iso)

        return iso

    __str__ = isoformat

    def toordinal(self):
        return self.to_gregorian().toordinal() - 226894

    @classmethod
    def fromordinal(cls, n):
        return cls(date.fromordinal(n + 226894))

    def __hash__(self):
        if self.__hashcode == -1:
            self.__hashcode = hash(self.__getstate__())

        return self.__hashcode

    def __getstate__(self):
        yhi, ylo = divmod(self.__year, 256)
        return bytes([yhi, ylo, self.__month, self.__day]),

    def __setstate__(self, string):
        if len(string) != 4 or not (1 <= string[2] <= 12):
            raise TypeError("not enough arguments")

        yhi, ylo, self.__month, self.__day = string
        self.__year = yhi * 256 + ylo

    def __reduce__(self):
        return self.__class__, self.__getstate__()

    def __repr__(self):
        return self.strftime("JalaliDate(%Y, %m, %d, %A)", "en")

    resolution = timedelta(1)

    def replace(self, year=None, month=None, day=None, locale=None):
        if year is None:
            year = self.__year

        if month is None:
            month = self.__month

        if day is None:
            day = self.__day

        if locale is None:
            locale = self.__locale

        return JalaliDate(year, month, day, locale)

    @classmethod
    def fromtimestamp(cls, timestamp):
        return cls(date.fromtimestamp(timestamp))

    def weekday(self):
        return (self.toordinal() + 4) % 7

    def __format__(self, fmt):
        if len(fmt) != 0:
            return self.strftime(fmt)

        return str(self)

    def isoweekday(self):
        return self.weekday() + 1

    def week_of_year(self):
        o = JalaliDate(self.__year, 1, 1).weekday()
        days = self.days_before_month(self.__month) + self.__day + o

        week_no, r = divmod(days, 7)

        if r > 0:
            week_no += 1

        return week_no

    def isocalendar(self):
        raise NotImplemented

    def ctime(self):
        return self.strftime("%c")

    def strftime(self, fmt, locale=None):
        if locale is None or locale not in ["fa", "en"]:
            locale = self.__locale

        month_names = MONTH_NAMES_EN if locale == "en" else MONTH_NAMES_FA
        month_names_abbr = MONTH_NAMES_ABBR_EN if locale == "en" else MONTH_NAMES_ABBR_FA
        day_names = WEEKDAY_NAMES_EN if locale == "en" else WEEKDAY_NAMES_FA
        day_names_abbr = WEEKDAY_NAMES_ABBR_EN if locale == "en" else WEEKDAY_NAMES_ABBR_FA
        am = "AM" if locale == "en" else "ق ظ"

        format_time = {
            "%a": day_names_abbr[self.weekday()],
            "%A": day_names[self.weekday()],

            "%w": str(self.weekday()),

            "%d": "%02d" % self.__day,
            "%-d": "%d" % self.__day,

            "%b": month_names_abbr[self.__month],
            "%B": month_names[self.__month],

            "%m": "%02d" % self.__month,
            "%-m": "%d" % self.__month,

            "%y": "%d" % (self.__year % 100),
            "%Y": "%d" % self.__year,

            "%H": "00",
            "%-H": "0",
            "%I": "00",
            "%-I": "0",

            "%p": am,

            "%M": "00",
            "%-M": "0",

            "%S": "00",
            "%-S": "0",

            "%f": "000000",

            "%z": "",
            "%Z": "",

            "%j": "%03d" % (self.days_before_month(self.__month) + self.__day),
            "%-j": "%d" % (self.days_before_month(self.__month) + self.__day),

            "%U": "%02d" % self.week_of_year(),
            "%W": "%d" % self.week_of_year(),

            "%X": "00:00:00",

            "%%": "%",
        }

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": self.strftime("%A %-d %B %Y")})

        if "%x" in fmt:
            fmt = utils.replace(fmt, {"%x": self.strftime("%y/%-m/%-d")})

        result = utils.replace(fmt, format_time)

        if locale == "fa":
            result = digits.en_to_fa(result)

        return result

    def _compare(self, other):
        assert isinstance(other, JalaliDate)

        y, m, d = self.__year, self.__month, self.__day
        y2, m2, d2 = other.__year, other.__month, other.__day

        return 0 if (y, m, d) == (y2, m2, d2) else 1 if (y, m, d) > (y2, m2, d2) else -1

    def __eq__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) == 0

        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) != 0

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) <= 0

        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) < 0

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) >= 0

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) > 0

        return NotImplemented

    def __add__(self, other):
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days

            if 0 < o <= _MAXORDINAL:
                return JalaliDate.fromordinal(o)

            raise OverflowError("result out of range")

        return NotImplemented

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

        return NotImplemented
