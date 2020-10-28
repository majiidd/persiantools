# -*- coding: utf-8 -*-
import sys
from datetime import date, timedelta, tzinfo, time as _time, datetime as dt
import operator

from persiantools import digits, utils, PY2

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
    [29, 30, 336],  # esfand
]


class JalaliDate(object):
    __slots__ = "_year", "_month", "_day", "_locale", "_hashcode"

    def __init__(self, year, month=None, day=None, locale="en"):
        if isinstance(year, JalaliDate) and month is None:
            month = year.month
            day = year.day
            locale = year.locale
            year = year.year

        elif isinstance(year, date):
            jdate = self.to_jalali(year)
            year, month, day = jdate.year, jdate.month, jdate.day

        elif (isinstance(year, bytes) and len(year) == 4 and 1 <= year[2] <= 12) or (
            isinstance(year, str) and year.startswith("[", 0, 1)
        ):
            if PY2:
                import ast

                self.__setstate__(ast.literal_eval(year))
            else:
                self.__setstate__(year)

            year = self._year
            month = self._month
            day = self._day

        year, month, day, locale = self._check_date_fields(year, month, day, locale)

        self._year = year
        self._month = month
        self._day = day
        self._locale = locale
        self._hashcode = -1

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, locale):
        assert locale in ("en", "fa"), "locale must be 'en' or 'fa'"
        self._locale = locale

    @classmethod
    def _check_date_fields(cls, year, month, day, locale):
        year = operator.index(year)
        month = operator.index(month)
        day = operator.index(day)

        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError("year must be in %d..%d" % (MINYEAR, MAXYEAR), year)

        if not 1 <= month <= 12:
            raise ValueError("month must be in 1..12", month)

        dim = cls.days_in_month(month, year)
        if not 1 <= day <= dim:
            raise ValueError("day must be in 1..%d" % dim, day)

        if locale not in ["en", "fa"]:
            raise ValueError("locale must be 'en' or 'fa'")

        return year, month, day, locale

    @classmethod
    def chack_date(cls, year, month, day):
        try:
            cls._check_date_fields(year, month, day, "en")
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
        assert 1 <= month <= 12, "month must be in 1..12"

        if month == 12 and cls.is_leap(year):
            return _MONTH_COUNT[month][1]

        return _MONTH_COUNT[month][0]

    @staticmethod
    def days_before_month(month):
        assert 1 <= month <= 12, "month must be in 1..12"

        return _MONTH_COUNT[month][2]

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
        days = (365 * year) + int((year2 + 3) / 4) - int((year2 + 99) / 100)
        days += int((year2 + 399) / 400) - 80 + day + g_d_m[month - 1]
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
        """based on jdf.scr.ir"""
        month = self.month
        day = self.day
        year = self.year

        gy = 621 if year <= 979 else 1600
        year -= 0 if year <= 979 else 979

        d = (month - 1) * 31 if month < 7 else ((month - 7) * 30) + 186
        days = (365 * year) + (int(year / 33) * 8) + int(((year % 33) + 3) / 4)
        days += 78 + day + d

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

        g_d_m = [
            0,
            31,
            29 if (gy % 4 == 0 and gy % 100 != 0) or gy % 400 == 0 else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ]
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
        "Return local time tuple compatible with time.localtime()."
        return self.to_gregorian().timetuple()

    def isoformat(self):
        iso = "%04d-%02d-%02d" % (self._year, self._month, self._day)

        if self._locale == "fa":
            iso = digits.en_to_fa(iso)

        return iso

    __str__ = isoformat

    def toordinal(self):
        return self.to_gregorian().toordinal() - 226894

    @classmethod
    def fromordinal(cls, n):
        return cls(date.fromordinal(n + 226894))

    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a date from the output of JalaliDate.isoformat()."""
        if not isinstance(date_string, str):
            raise TypeError("fromisoformat: argument must be str")

        return cls(*cls._parse_isoformat_date(digits.fa_to_en(date_string)))

    @classmethod
    def _parse_isoformat_date(cls, dtstr):
        # It is assumed that this function will only be called with a
        # string of length exactly 10, and (though this is not used) ASCII-only
        year = int(dtstr[0:4])
        if dtstr[4] != "-":
            raise ValueError("Invalid date separator: %s" % dtstr[4])

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
        return "JalaliDate(%d, %d, %d, %s)" % (
            self._year,
            self._month,
            self._day,
            WEEKDAY_NAMES_EN[self.weekday()],
        )

    resolution = timedelta(1)

    def replace(self, year=None, month=None, day=None, locale=None):
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
    def fromtimestamp(cls, timestamp):
        return cls(date.fromtimestamp(timestamp))

    def weekday(self):
        return (self.toordinal() + 4) % 7

    def __format__(self, fmt):
        if not isinstance(fmt, str):
            raise TypeError("must be str, not %s" % type(fmt).__name__)
        if len(fmt) != 0:
            return self.strftime(fmt)

        return str(self)

    def isoweekday(self):
        return self.weekday() + 1

    def week_of_year(self):
        o = JalaliDate(self._year, 1, 1).weekday()
        days = self.days_before_month(self._month) + self._day + o

        week_no, r = divmod(days, 7)

        if r > 0:
            week_no += 1

        return week_no

    def isocalendar(self):
        """Return a 3-tuple containing ISO year, week number, and weekday."""
        return self.year, self.week_of_year(), self.isoweekday()

    def ctime(self):
        return self.strftime("%c")

    def strftime(self, fmt, locale=None):
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
            "%d": "%02d" % self._day,
            "%b": month_names_abbr[self._month],
            "%B": month_names[self._month],
            "%m": "%02d" % self._month,
            "%y": "%02d" % (self._year % 100),
            "%Y": "%04d" % self._year,
            "%H": "00",
            "%I": "00",
            "%p": am,
            "%M": "00",
            "%S": "00",
            "%f": "000000",
            "%z": "",
            "%Z": "",
            "%j": "%03d" % (self.days_before_month(self._month) + self._day),
            "%U": "%02d" % self.week_of_year(),
            "%W": "%02d" % self.week_of_year(),
            "%X": "00:00:00",
            "%%": "%",
        }

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": self.strftime("%A %d %B %Y")})

        if "%x" in fmt:
            fmt = utils.replace(fmt, {"%x": self.strftime("%y/%m/%d")})

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

        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, JalaliDate):
            return self._compare(other) != 0
        elif isinstance(other, date):
            return self._compare(JalaliDate(other)) != 0

        raise NotImplementedError

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
        """Subtract two JalaliDates/dates, or a JalaliDate/date and a timedelta."""
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

        elif (isinstance(year, bytes) and len(year) == 10) or (
            isinstance(year, str) and year.startswith("[", 0, 1)
        ):
            if PY2:
                import ast

                self.__setstate__(ast.literal_eval(year), month)
            else:
                self.__setstate__(year, month)

            year = self._year
            month = self._month
            day = self._day
            hour = self._hour
            minute = self._minute
            second = self._second
            microsecond = self._microsecond
            tzinfo = self._tzinfo

        super(JalaliDateTime, self).__init__(year, month, day, locale)
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
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def microsecond(self):
        return self._microsecond

    @property
    def tzinfo(self):
        return self._tzinfo

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        return cls(dt.fromtimestamp(t, tz))

    @classmethod
    def utcfromtimestamp(cls, t):
        return cls(dt.utcfromtimestamp(t))

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
        return cls(dt.utcnow())

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
        if sys.version_info >= (3, 3):
            return self.to_gregorian().timestamp()
        else:
            gregorian_dt = self.to_gregorian()
            return (gregorian_dt - dt(1970, 1, 1, tzinfo=gregorian_dt.tzinfo)).total_seconds()

    def utctimetuple(self):
        "Return UTC time tuple compatible with time.gmtime()."
        return self.to_gregorian().utctimetuple()

    def astimezone(self, tz=None):
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

    def isoformat(self, sep="T"):
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

        name = getattr(self._tzinfo, "tzname")(self.to_gregorian())

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
            raise TypeError(
                "tzinfo.%s() must return None " "or timedelta, not '%s'" % (name, type(offset))
            )

        if offset % timedelta(minutes=1) or offset.microseconds:
            raise ValueError(
                "tzinfo.%s() must return a whole number " "of minutes, got %s" % (name, offset)
            )

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
        g_date = super(JalaliDateTime, self).to_gregorian()

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
    def strptime(cls, data_string, fmt):
        raise NotImplementedError

    def __repr__(self):
        """Convert to formal string, for repr()."""
        l = [
            self._year,
            self._month,
            self._day,  # These are never zero
            self._hour,
            self._minute,
            self._second,
            self._microsecond,
        ]

        if l[-1] == 0:
            del l[-1]

        if l[-1] == 0:
            del l[-1]

        s = ", ".join(map(str, l))
        s = "%s(%s)" % ("JalaliDateTime", s)

        if self._tzinfo is not None:
            assert s[-1:] == ")"
            s = s[:-1] + ", tzinfo=%r" % self._tzinfo + ")"

        return s

    def __str__(self):
        return self.isoformat(sep=" ")

    def strftime(self, fmt):
        datetime = self.to_gregorian()

        format_time = {
            "%H": "%02d" % self._hour,
            "%I": "%02d" % (self._hour if self._hour <= 12 else self._hour - 12),
            "%p": "AM" if self._hour < 12 else "PM",
            "%M": "%02d" % self._minute,
            "%S": "%02d" % self._second,
            "%f": "%06d" % self._microsecond,
            "%z": datetime.strftime("%z"),
            "%Z": ("" if not self._tzinfo else self._tzinfo.tzname(self)),
            "%X": "%02d:%02d:%02d" % (self._hour, self._minute, self._second),
        }

        if "%c" in fmt:
            fmt = utils.replace(fmt, {"%c": self.strftime("%A %d %B %Y %X")})

        result = utils.replace(fmt, format_time)

        result = super(JalaliDateTime, self).strftime(result, "en")

        return result

    def __base_compare(self, other):
        assert isinstance(other, JalaliDateTime)

        y, m, d, h, m, s, ms = [
            self._year,
            self._month,
            self._day,
            self._hour,
            self._minute,
            self._second,
            self._microsecond,
        ]
        y2, m2, d2, h2, m2, s2, ms2 = [
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
            if (y, m, d, h, m, s, ms) == (y2, m2, d2, h2, m2, s2, ms2)
            else 1
            if (y, m, d, h, m, s, ms) > (y2, m2, d2, h2, m2, s2, ms2)
            else -1
        )

    def _cmp(self, other, allow_mixed=False):
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
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other, allow_mixed=True) != 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other), allow_mixed=True) != 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            return True

    def __le__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) <= 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) <= 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(
                "can't compare '%s' to '%s'" % (type(self).__name__, type(other).__name__)
            )

    def __lt__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) < 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) < 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(
                "can't compare '%s' to '%s'" % (type(self).__name__, type(other).__name__)
            )

    def __ge__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) >= 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) >= 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(
                "can't compare '%s' to '%s'" % (type(self).__name__, type(other).__name__)
            )

    def __gt__(self, other):
        if isinstance(other, JalaliDateTime):
            return self._cmp(other) > 0
        elif isinstance(other, dt):
            return self._cmp(JalaliDateTime(other)) > 0
        elif not isinstance(other, (JalaliDate, date)):
            raise NotImplementedError
        else:
            raise TypeError(
                "can't compare '%s' to '%s'" % (type(self).__name__, type(other).__name__)
            )

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
