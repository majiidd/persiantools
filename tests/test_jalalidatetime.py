import os
import pickle
import time
from datetime import date, datetime
from datetime import time as _time
from datetime import timedelta, timezone
from unittest import TestCase

import pytest
import pytz

from persiantools.jdatetime import JalaliDate, JalaliDateTime, _is_ascii_digit


class TestJalaliDateTime(TestCase):
    def test_shamsi_to_gregorian(self):
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 14, 0, 0, 0).to_gregorian(),
            datetime(1988, 5, 4, 14, 0, 0, 0),
        )
        self.assertEqual(
            JalaliDateTime(1399, 11, 23, 13, 12, 0, 0).to_gregorian(),
            datetime(2021, 2, 11, 13, 12, 0, 0),
        )
        self.assertEqual(
            JalaliDateTime(1404, 1, 1, 13, 12, 0, 0).to_gregorian(),
            datetime(2025, 3, 21, 13, 12, 0, 0),
        )

    def test_gregorian_to_shamsi(self):
        self.assertEqual(
            JalaliDateTime(datetime(1990, 9, 23, 14, 14, 1, 1111)),
            JalaliDateTime(1369, 7, 1, 14, 14, 1, 1111),
        )
        self.assertEqual(
            JalaliDateTime.to_jalali(datetime(1988, 5, 4, 14, 0, 0, 0)),
            JalaliDateTime(1367, 2, 14, 14, 0, 0, 0),
        )

    def test_base(self):
        self.assertEqual(
            JalaliDateTime(1369, 7, 1, 14, 14, 1, 9111),
            JalaliDateTime(JalaliDateTime(1369, 7, 1, 14, 14, 1, 9111)),
        )

        g = JalaliDateTime.now()
        self.assertEqual(g.time(), _time(g.hour, g.minute, g.second, g.microsecond))

        g = g.replace(tzinfo=pytz.timezone("America/Los_Angeles"))
        self.assertEqual(
            g.timetz(),
            _time(
                g.hour,
                g.minute,
                g.second,
                g.microsecond,
                pytz.timezone("America/Los_Angeles"),
            ),
        )

        self.assertEqual(
            JalaliDateTime.fromtimestamp(578723400, pytz.utc),
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc),
        )
        self.assertEqual(
            JalaliDateTime.utcfromtimestamp(578723400),
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, tzinfo=timezone.utc),
        )

        with pytest.raises(TypeError):
            JalaliDateTime._check_time_fields("20", 1, 61, 1000)

        with pytest.raises(ValueError):
            JalaliDateTime(1367, 2, 14, 25, 0, 0, 0)

        with pytest.raises(ValueError):
            JalaliDateTime(1367, 2, 14, 22, 61, 0, 0)

        with pytest.raises(ValueError):
            JalaliDateTime(1367, 2, 14, 22, 1, 722, 0)

        with pytest.raises(ValueError):
            JalaliDateTime(1367, 2, 14, 22, 1, 0, 1000000)

    def test_timetuple(self):
        self.assertEqual(
            JalaliDateTime(1398, 3, 17, 18, 36, 30, 811090).timetuple(),
            time.struct_time((2019, 6, 7, 18, 36, 30, 4, 158, -1)),
        )
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 14, 0, 0, 0).utctimetuple(),
            time.struct_time((1988, 5, 4, 14, 0, 0, 2, 125, 0)),
        )

    def test_check_utc_offset(self):
        JalaliDateTime.check_utc_offset("utcoffset", None)
        JalaliDateTime.check_utc_offset("dst", None)

        offset = timedelta(minutes=30)
        JalaliDateTime.check_utc_offset("utcoffset", offset)
        JalaliDateTime.check_utc_offset("dst", offset)

        with pytest.raises(AssertionError):
            JalaliDateTime.check_utc_offset("invalid", timedelta(minutes=30))

        with pytest.raises(TypeError):
            JalaliDateTime.check_utc_offset("utcoffset", 30)

        with pytest.raises(ValueError):
            JalaliDateTime.check_utc_offset("dst", timedelta(seconds=61))

    def test_others(self):
        self.assertTrue(JalaliDateTime.fromtimestamp(time.time() - 10) <= JalaliDateTime.now())
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc).timestamp(), 578723400)
        self.assertEqual(
            JalaliDateTime.fromtimestamp(578723400, pytz.utc),
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc),
        )
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).jdate(), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).date(), date(1988, 5, 4))
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).replace(tzinfo=pytz.utc).__repr__(),
            "JalaliDateTime(1367, 2, 14, 4, 30, tzinfo=<UTC>)",
        )
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).replace(year=1395, day=3, minute=59),
            JalaliDateTime(1395, 2, 3, 4, 59, 4, 4444),
        )

        self.assertEqual(JalaliDateTime.now(pytz.utc).tzname(), "UTC")
        self.assertIsNone(JalaliDateTime.today().tzname())
        self.assertIsNone(JalaliDateTime.today().dst())

        dt = JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc)
        self.assertEqual(dt.dst(), timedelta(0))

        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).ctime(),
            "Chaharshanbeh 14 Ordibehesht 1367 04:30:00",
        )
        self.assertEqual(
            JalaliDateTime(1396, 7, 27, 21, 48, 0, 0).ctime(),
            "Panjshanbeh 27 Mehr 1396 21:48:00",
        )
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).replace(locale="fa").ctime(),
            "چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۰۴:۳۰:۰۰",
        )
        self.assertEqual(
            JalaliDateTime(1397, 12, 1, 23, 32, 0, 0).replace(locale="fa").ctime(),
            "چهارشنبه ۰۱ اسفند ۱۳۹۷ ۲۳:۳۲:۰۰",
        )

        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 1, pytz.utc).isoformat(),
            "1367-02-14T04:30:00.000001+00:00",
        )
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 1, pytz.utc).__str__(),
            "1367-02-14 04:30:00.000001+00:00",
        )

    def test_operators(self):
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) + timedelta(days=30, seconds=15, milliseconds=1),
            JalaliDateTime(1367, 3, 13, 4, 30, 15, 1000),
        )
        self.assertEqual(
            JalaliDateTime(1397, 12, 27, 4, 30, 0, 0) + timedelta(days=4),
            JalaliDateTime(1398, 1, 2, 4, 30, 0, 0),
        )
        self.assertEqual(
            JalaliDateTime(1395, 2, 14, 4, 30, 0, 0) - JalaliDateTime(1367, 2, 14, 4, 30, 0, 0),
            timedelta(days=10226),
        )
        self.assertEqual(
            JalaliDateTime(1395, 2, 14, 4, 30, 0, 0) - datetime(1988, 5, 4, 4, 30, 0, 0),
            timedelta(days=10226),
        )
        self.assertEqual(
            JalaliDateTime(1395, 4, 16, 20, 14, 30, 0) - timedelta(days=1, seconds=31),
            JalaliDateTime(1395, 4, 15, 20, 13, 59, 0),
        )

        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) == JalaliDateTime(1367, 2, 14, 4, 30, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) == datetime(1988, 5, 4, 4, 30, 0, 0))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) == date(1988, 5, 4))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) == JalaliDate(1988, 5, 4))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) != JalaliDateTime(1367, 2, 14, 4, 30, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) != datetime(1989, 5, 4, 4, 30, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) != date(1988, 5, 4))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) != JalaliDate(1367, 5, 5))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) < JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) < datetime(1988, 5, 4, 4, 30, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) < JalaliDateTime(1367, 3, 14, 4, 30, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) <= JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) <= datetime(1988, 5, 4, 4, 30, 0, 100))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) > JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) > datetime(2019, 10, 11, 0, 30, 0, 100))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) >= JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) >= datetime(1988, 5, 4, 0, 0, 0, 0))
        self.assertTrue(JalaliDateTime(1395, 4, 15, 20, 13, 59, 0) == JalaliDateTime(1395, 4, 15, 20, 13, 59, 0))
        self.assertTrue(
            JalaliDateTime(1395, 4, 15, 20, 13, 59, 0, pytz.utc) != JalaliDateTime(1395, 4, 15, 20, 13, 59, 0)
        )

        self.assertEqual(
            JalaliDateTime(1395, 4, 16, 20, 14, 30, 0, pytz.utc)
            - JalaliDateTime(1395, 4, 16, 20, 14, 30, 0, pytz.timezone("Asia/Tehran")),
            pytz.timezone("Asia/Tehran")._utcoffset,
        )

        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) == {"year": 1367})
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) == "")
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) != "string")

        with pytest.raises(NotImplementedError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) < 1.55

        with pytest.raises(TypeError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) < date(1988, 4, 5)

        with pytest.raises(NotImplementedError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) <= 100

        with pytest.raises(TypeError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) <= JalaliDate(1367, 5, 5)

        with pytest.raises(NotImplementedError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) > timedelta(days=30)

        with pytest.raises(TypeError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) > date(1988, 4, 5)

        with pytest.raises(NotImplementedError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) >= pytz.utc

        with pytest.raises(TypeError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) >= JalaliDate(1392, 4, 5)

        with pytest.raises(NotImplementedError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) + JalaliDateTime(1367, 2, 14, 0, 0, 0, 0)

        with pytest.raises(NotImplementedError):
            assert JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) - []

    def test_hash(self):
        j1 = JalaliDateTime.today().replace(tzinfo=pytz.utc)
        j2 = JalaliDateTime(1369, 7, 1, 0, 0, 0, 0)
        j3 = JalaliDateTime(datetime(1990, 9, 23, 0, 0, 0, 0))

        self.assertEqual(
            {j1: "today", j2: "test1", j3: "test2"},
            {
                JalaliDateTime(
                    j1.year,
                    j1.month,
                    j1.day,
                    j1.hour,
                    j1.minute,
                    j1.second,
                    j1.microsecond,
                    j1.tzinfo,
                ): "today",
                JalaliDateTime(1369, 7, 1, 0, 0, 0, 0): "test2",
            },
        )

    def test_pickle(self):
        file = open("save.p", "wb")
        now = JalaliDateTime.now().replace(tzinfo=pytz.timezone("Asia/Tehran"))
        pickle.dump(now, file)
        file.close()

        file2 = open("save.p", "rb")
        j = pickle.load(file2)  # nosec B301
        file2.close()

        self.assertEqual(j, now)

        os.remove("save.p")

    def test_format(self):
        self.assertEqual(
            JalaliDateTime(1369, 7, 1, 14, 0, 10, 0, pytz.utc).strftime("%X %p %z %Z"),
            "14:00:10 PM +0000 UTC",
        )

        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 14, 0, 10, 0, pytz.utc).strftime("%c"),
            "Chaharshanbeh 14 Ordibehesht 1367 14:00:10",
        )

        self.assertEqual(
            JalaliDateTime(1397, 11, 30, 14, 0, 10, 0, pytz.utc).strftime("%c"),
            "Seshanbeh 30 Bahman 1397 14:00:10",
        )

        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 11, 0, 10, 553, pytz.utc).strftime("%I:%M:%S.%f %p"),
            "11:00:10.000553 AM",
        )

        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 14, 0, 10, 553, pytz.utc).strftime("%I:%M:%S.%f %p"),
            "02:00:10.000553 PM",
        )

        jdt = JalaliDateTime(1367, 2, 14, 10, 10, 10, 10, locale="fa")
        self.assertEqual(jdt.strftime("%c"), "چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۱۰:۱۰:۱۰")

        jdt = JalaliDateTime(1367, 2, 14, 10, 10, 10, 10)
        self.assertEqual(jdt.strftime("%c", "fa"), "چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۱۰:۱۰:۱۰")

        jdt = JalaliDateTime(1400, 4, 25, 21, 45, 0, 0, locale="fa")
        self.assertEqual(jdt.strftime("%c"), "جمعه ۲۵ تیر ۱۴۰۰ ۲۱:۴۵:۰۰")

    def test_strptime(self):
        self.assertEqual(
            JalaliDateTime(1400, 6, 23, 1, 4, 1),
            JalaliDateTime.strptime("1400-06-23 01:04:01 am", "%Y-%m-%d %I:%M:%S %p"),
        )
        self.assertEqual(JalaliDateTime(1374, 4, 8, 13, 45, 10), JalaliDateTime.strptime("1374/4/8 13:45:10", "%x %X"))
        self.assertEqual(
            JalaliDateTime(1400, 1, 11, 23, 16, 7), JalaliDateTime.strptime("1400-01-11 23:16:07", "%Y-%m-%d %X")
        )
        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 1, 1, 1), JalaliDateTime.strptime("1367/02/14 01:01:01", "%Y/%m/%d %X")
        )

        persian_month = "اسفند"
        persian_period = "ب.ظ"
        self.assertEqual(
            JalaliDateTime(1379, 12, 1, 23, 16, 37),
            JalaliDateTime.strptime(
                f"1 {persian_month} 1379 11:16 {persian_period} 37", "%d %B %Y %I:%M %p %S", locale="fa"
            ),
        )

        self.assertEqual(
            JalaliDateTime(1367, 2, 14, 10, 10, 10),
            JalaliDateTime.strptime("چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۱۰:۱۰:۱۰", "%c", locale="fa"),
        )
        self.assertEqual(
            JalaliDateTime(1400, 1, 1, 14, 0, 10, 553),
            JalaliDateTime.strptime("1400-01-01 02:00:10.000553 PM", "%Y-%m-%d %I:%M:%S.%f %p"),
        )

        jdt = JalaliDateTime(1374, 4, 8, 16, 28, 3, 227, pytz.utc)
        self.assertEqual(jdt, JalaliDateTime.strptime(jdt.strftime("%c %f %z %Z"), "%c %f %z %Z"))

        jdt_utc_combined = JalaliDateTime(1374, 4, 8, 16, 28, 3, 227, timezone.utc)
        self.assertEqual(
            jdt_utc_combined, JalaliDateTime.strptime(jdt_utc_combined.strftime("%c %f %z %Z"), "%c %f %z %Z")
        )

    def test_strptime_basic(self):
        date_string = "1400-01-01 12:30:45"
        fmt = "%Y-%m-%d %H:%M:%S"
        jdt = JalaliDateTime.strptime(date_string, fmt)
        self.assertEqual(jdt.year, 1400)
        self.assertEqual(jdt.month, 1)
        self.assertEqual(jdt.day, 1)
        self.assertEqual(jdt.hour, 12)
        self.assertEqual(jdt.minute, 30)
        self.assertEqual(jdt.second, 45)

    def test_strptime_with_timezone(self):
        date_string = "1400-01-01 12:30:45 +0330"
        fmt = "%Y-%m-%d %H:%M:%S %z"
        jdt = JalaliDateTime.strptime(date_string, fmt)
        self.assertEqual(jdt.year, 1400)
        self.assertEqual(jdt.month, 1)
        self.assertEqual(jdt.day, 1)
        self.assertEqual(jdt.hour, 12)
        self.assertEqual(jdt.minute, 30)
        self.assertEqual(jdt.second, 45)
        self.assertEqual(jdt.utcoffset(), timedelta(hours=3, minutes=30))

    def test_strptime_z_directive_valid_formats(self):
        base_dt_str = "1400-01-01 10:00:00"
        fmt_base = "%Y-%m-%d %H:%M:%S"

        valid_z_formats = [
            ("+0330", 3, 30),
            ("-0500", -5, 0),
            ("+0430", 4, 30),
            ("-0715", -7, -15),
            ("+0000", 0, 0),
            ("-0000", 0, 0),
            ("+1400", 14, 0),
            ("-1400", -14, 0),
            ("+0059", 0, 59),
        ]

        for tz_str, hours, minutes in valid_z_formats:
            date_string = f"{base_dt_str} {tz_str}"
            fmt = f"{fmt_base} %z"
            with self.subTest(date_string=date_string, fmt=fmt):
                jdt = JalaliDateTime.strptime(date_string, fmt)
                self.assertIsNotNone(jdt.tzinfo, f"tzinfo should not be None for {date_string}")
                self.assertIsInstance(jdt.tzinfo, timezone, f"tzinfo should be datetime.timezone for {date_string}")
                expected_offset = timedelta(hours=hours, minutes=minutes)
                self.assertEqual(jdt.utcoffset(), expected_offset, f"Offset mismatch for {date_string}")
                self.assertEqual(jdt.year, 1400)
                self.assertEqual(jdt.hour, 10)

    def test_strptime_z_directive_invalid_formats(self):
        base_dt_str = "1400-01-01 10:00:00"
        fmt_base = "%Y-%m-%d %H:%M:%S"

        invalid_z_formats = [
            "0330",  # Missing sign: In Python, the %z directive requires a leading '+' or '-' for the timezone offset.
            "+330",  # Incorrect number of digits (hour)
            "+033",  # Incorrect number of digits (minute)
            "+03:3",  # Incorrect number of digits (minute with colon)
            "+03-30",  # Invalid separator
            "03:30",  # Missing sign with colon
            "+03:300",  # Too many minute digits
            "+030:30",  # Too many hour digits
            "+0A30",  # Non-numeric hour
            "+03B0",  # Non-numeric minute
            "+2500",  # Hour out of range (max is +2359 or +1400 for this specific regex in Python for %z)
            "+2400",  # Hour part out of range (>=24)
            "-2400",
            "+0360",  # Minute part out of range (>=60)
            "-0360",
            "+03:60",
            " +0330",  # Leading space before offset
            "+0330 ",  # Trailing space after offset (will cause full string match failure)
            "GMT+0330",  # Non-standard prefix
        ]

        for tz_str in invalid_z_formats:
            date_string = f"{base_dt_str} {tz_str}"
            fmt = f"{fmt_base} %z"
            with self.subTest(date_string=date_string, fmt=fmt):
                with self.assertRaises(ValueError, msg=f"Failed for invalid tz string: {tz_str}"):
                    JalaliDateTime.strptime(date_string, fmt)

        # Test %z without enough characters following
        with self.assertRaises(ValueError):
            JalaliDateTime.strptime(f"{base_dt_str} +", f"{fmt_base} %z")
        with self.assertRaises(ValueError):
            JalaliDateTime.strptime(f"{base_dt_str} +03", f"{fmt_base} %z")

    def test_strptime_z_directive_locale_independence(self):
        base_dt_str = "1400-01-01 10:00:00"
        tz_str = "+0545"
        fmt = "%Y-%m-%d %H:%M:%S %z"
        date_string = f"{base_dt_str} {tz_str}"
        expected_offset = timedelta(hours=5, minutes=45)

        # Test with locale 'en'
        jdt_en = JalaliDateTime.strptime(date_string, fmt, locale="en")
        self.assertIsNotNone(jdt_en.tzinfo)
        self.assertEqual(jdt_en.utcoffset(), expected_offset)
        self.assertEqual(jdt_en.year, 1400)

        # Test with locale 'fa'
        jdt_fa = JalaliDateTime.strptime(date_string, fmt, locale="fa")
        self.assertIsNotNone(jdt_fa.tzinfo)
        self.assertEqual(jdt_fa.utcoffset(), expected_offset)
        self.assertEqual(jdt_fa.year, 1400)

        date_string_fa_main = f"۱۴۰۰-۰۱-۰۱ ۱۰:۰۰:۰۰ {tz_str}"
        jdt_fa_main = JalaliDateTime.strptime(date_string_fa_main, fmt, locale="fa")
        self.assertIsNotNone(jdt_fa_main.tzinfo)
        self.assertEqual(jdt_fa_main.utcoffset(), expected_offset)
        self.assertEqual(jdt_fa_main.year, 1400)

    def test_strptime_with_locale_fa(self):
        date_string = "۱۴۰۰-۰۱-۰۱ ۱۲:۳۰:۴۵"
        fmt = "%Y-%m-%d %H:%M:%S"
        jdt = JalaliDateTime.strptime(date_string, fmt, locale="fa")
        self.assertEqual(jdt.year, 1400)
        self.assertEqual(jdt.month, 1)
        self.assertEqual(jdt.day, 1)
        self.assertEqual(jdt.hour, 12)
        self.assertEqual(jdt.minute, 30)
        self.assertEqual(jdt.second, 45)

    def test_strptime_invalid_format(self):
        date_string = "1400/01/01"
        fmt = "%Y-%m-%d"
        with self.assertRaises(ValueError):
            JalaliDateTime.strptime(date_string, fmt)

    def test_strptime_invalid_locale(self):
        date_string = "1400-01-01 12:30:45"
        fmt = "%Y-%m-%d %H:%M:%S"
        with self.assertRaises(ValueError):
            JalaliDateTime.strptime(date_string, fmt, locale="invalid")

    def test_utcnow(self):
        now_utc = datetime.now(timezone.utc)
        jalali_now = JalaliDateTime.utcnow()
        gregorian_now = jalali_now.to_gregorian()

        self.assertTrue(
            abs(now_utc - gregorian_now) < timedelta(seconds=1),
            f"Expected the times to be close. now_utc: {now_utc}, gregorian_now: {gregorian_now}",
        )

    def test_check_tzinfo_arg_valid(self):
        JalaliDateTime._check_tzinfo_arg(None)
        JalaliDateTime._check_tzinfo_arg(timezone.utc)

    def test_check_tzinfo_arg_invalid(self):
        with self.assertRaises(TypeError):
            JalaliDateTime._check_tzinfo_arg(123)

        with self.assertRaises(TypeError):
            JalaliDateTime._check_tzinfo_arg("InvalidTzinfo")

    def test_combine(self):
        jdate = JalaliDate(1367, 2, 14)
        time_v = _time(4, 30, 1)
        combined = JalaliDateTime.combine(jdate, time_v)

        self.assertEqual(combined.year, 1367)
        self.assertEqual(combined.month, 2)
        self.assertEqual(combined.day, 14)
        self.assertEqual(combined.hour, 4)
        self.assertEqual(combined.minute, 30)
        self.assertEqual(combined.second, 1)

        with self.assertRaises(TypeError):
            JalaliDateTime.combine("InvalidDate", _time(12, 30, 45))

        jdate = JalaliDate(1400, 1, 1)
        with self.assertRaises(TypeError):
            JalaliDateTime.combine(jdate, "InvalidTime")

    def test_astimezone_utc(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=3)))
        jdt_utc = jdt.astimezone(timezone.utc)

        gregorian_utc = jdt_utc.to_gregorian()
        expected_utc = datetime(2021, 3, 21, 9, 30, 45, tzinfo=timezone.utc)

        self.assertEqual(gregorian_utc, expected_utc)

    def test_astimezone_other(self):
        jdt = JalaliDateTime(1400, 1, 1, 20, 30, 45, tzinfo=timezone.utc)
        new_tz = timezone(timedelta(hours=5))
        jdt_new_tz = jdt.astimezone(new_tz)

        gregorian_new_tz = jdt_new_tz.to_gregorian()
        expected_new_tz = datetime(2021, 3, 22, 1, 30, 45, tzinfo=new_tz)  # 5 hours added, next day

        self.assertEqual(gregorian_new_tz, expected_new_tz)

    def test_astimezone_invalid(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        with self.assertRaises(TypeError):
            jdt.astimezone("InvalidTimezone")

    def test_isoformat_positive_offset(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=3, minutes=30)))
        iso_format = jdt.isoformat()
        expected_iso_format = "1400-01-01T12:30:45+03:30"
        self.assertEqual(iso_format, expected_iso_format)

    def test_isoformat_negative_offset(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(-timedelta(hours=4, minutes=45)))
        iso_format = jdt.isoformat()
        expected_iso_format = "1400-01-01T12:30:45-04:45"
        self.assertEqual(iso_format, expected_iso_format)

    def test_isoformat_no_offset(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45)
        iso_format = jdt.isoformat()
        expected_iso_format = "1400-01-01T12:30:45"
        self.assertEqual(iso_format, expected_iso_format)

    def test_isoformat_utc(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        iso_format = jdt.isoformat()
        expected_iso_format = "1400-01-01T12:30:45+00:00"
        self.assertEqual(iso_format, expected_iso_format)

    def test_cmp_naive_vs_aware(self):
        jdt_naive = JalaliDateTime(1400, 1, 1, 12, 30, 45)
        jdt_aware = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)

        with self.assertRaises(TypeError):
            jdt_naive._cmp(jdt_aware)

    def test_cmp_aware_vs_naive(self):
        jdt_naive = JalaliDateTime(1400, 1, 1, 12, 30, 45)
        jdt_aware = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)

        with self.assertRaises(TypeError):
            jdt_aware._cmp(jdt_naive)

    def test_cmp_aware_with_different_offsets(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=3)))
        jdt2 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=5)))

        self.assertEqual(jdt1._cmp(jdt2), 1)
        self.assertEqual(jdt2._cmp(jdt1), -1)

    def test_cmp_aware_with_same_offset(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        jdt2 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)

        self.assertEqual(jdt1._cmp(jdt2), 0)

    def test_cmp_diff_days(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        jdt2 = JalaliDateTime(1400, 1, 2, 12, 30, 45, tzinfo=timezone.utc)

        self.assertEqual(jdt1._cmp(jdt2), -1)
        self.assertEqual(jdt2._cmp(jdt1), 1)

    def test_cmp_diff_seconds(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        jdt2 = JalaliDateTime(1400, 1, 1, 12, 30, 46, tzinfo=timezone.utc)

        self.assertEqual(jdt1._cmp(jdt2), -1)
        self.assertEqual(jdt2._cmp(jdt1), 1)

    def test_subtract_same_offset(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 46, tzinfo=timezone.utc)
        jdt2 = JalaliDateTime(1400, 1, 1, 10, 30, 45, tzinfo=timezone.utc)

        result = jdt1 - jdt2
        expected = timedelta(hours=2, seconds=1)

        self.assertEqual(result, expected)

    def test_subtract_different_offset(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=3)))
        jdt2 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone(timedelta(hours=5)))

        result = jdt1 - jdt2
        expected = timedelta(hours=2)  # jdt1 is 2 hours behind jdt2

        self.assertEqual(result, expected)

    def test_subtract_naive_and_aware(self):
        jdt1 = JalaliDateTime(1400, 1, 1, 12, 30, 45)
        jdt2 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)

        with self.assertRaises(TypeError):
            _ = jdt1 - jdt2

    def test_subtract_with_timedelta(self):
        jdt = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        delta = timedelta(days=1, hours=1, minutes=30, seconds=15)

        result = jdt - delta
        expected = JalaliDateTime(1399, 12, 30, 11, 0, 30, tzinfo=timezone.utc)

        self.assertEqual(result, expected)

    def test_subtract_different_dates(self):
        jdt1 = JalaliDateTime(1400, 1, 2, 12, 30, 45, tzinfo=timezone.utc)
        jdt2 = JalaliDateTime(1400, 1, 1, 12, 30, 45, tzinfo=timezone.utc)

        result = jdt1 - jdt2
        expected = timedelta(days=1)

        self.assertEqual(result, expected)

    def test_to_jalali_with_timezone(self):
        dt = datetime.now(timezone.utc)
        jdate = JalaliDateTime.to_jalali(dt)
        self.assertEqual(jdate.tzinfo, timezone.utc)

    def test_strftime_basic(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45)
        self.assertEqual(jdate.strftime("%Y-%m-%d %H:%M:%S"), "1400-01-01 15:30:45")

    def test_strftime_locale_fa(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45, locale="fa")
        self.assertEqual(jdate.strftime("%Y-%m-%d %H:%M:%S", locale="fa"), "۱۴۰۰-۰۱-۰۱ ۱۵:۳۰:۴۵")

    def test_strftime_with_timezone_utc(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45, tzinfo=timezone.utc)
        self.assertEqual(jdate.strftime("%Y-%m-%d %H:%M:%S %Z"), "1400-01-01 15:30:45 UTC")

    def test_strftime_with_timezone_offset(self):
        tz = timezone(timedelta(hours=3, minutes=30))
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45, tzinfo=tz)
        self.assertEqual(jdate.strftime("%Y-%m-%d %H:%M:%S %z"), "1400-01-01 15:30:45 +0330")

    def test_strftime_with_abbreviated_month_day(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45)
        self.assertEqual(jdate.strftime("%b %a"), "Far Yek")

    def test_strftime_with_full_month_day(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45)
        self.assertEqual(jdate.strftime("%B %A"), "Farvardin Yekshanbeh")

    def test_strftime_with_custom_format(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45)
        self.assertEqual(jdate.strftime("%d %B %Y - %H:%M"), "01 Farvardin 1400 - 15:30")

    def test_strftime_with_persian_locale(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45, locale="fa")
        self.assertEqual(jdate.strftime("%A, %d %B %Y - %H:%M", locale="fa"), "یکشنبه, ۰۱ فروردین ۱۴۰۰ - ۱۵:۳۰")

    def test_strftime_with_periodic_time(self):
        jdate = JalaliDateTime(1400, 1, 1, 15, 30, 45)
        self.assertEqual(jdate.strftime("%I:%M %p"), "03:30 PM")

    def test_strftime_edge_case_midnight(self):
        jdate = JalaliDateTime(1400, 1, 1, 0, 0, 0)
        self.assertEqual(jdate.strftime("%Y-%m-%d %H:%M:%S"), "1400-01-01 00:00:00")

    def test_fromisoformat_valid_date_and_time(self):
        jdt = JalaliDateTime.fromisoformat("1403-08-09T02:21:45.123456+04:30")
        self.assertEqual(jdt.year, 1403)
        self.assertEqual(jdt.month, 8)
        self.assertEqual(jdt.day, 9)
        self.assertEqual(jdt.hour, 2)
        self.assertEqual(jdt.minute, 21)
        self.assertEqual(jdt.second, 45)
        self.assertEqual(jdt.microsecond, 123456)
        self.assertEqual(jdt.tzinfo, timezone(timedelta(hours=4, minutes=30)))

    def test_fromisoformat_with_timezone(self):
        jdt = JalaliDateTime.fromisoformat("1403-08-09T02:21:45+04:30")
        self.assertEqual(jdt.tzinfo, timezone(timedelta(hours=4, minutes=30)))

    def test_fromisoformat_invalid_string(self):
        with self.assertRaises(ValueError):
            JalaliDateTime.fromisoformat("invalid-date-time")

        self.assertEqual(JalaliDateTime._find_isoformat_datetime_separator("2021W12"), 7)

        with pytest.raises(ValueError, match="Invalid ISO string"):
            JalaliDateTime._find_isoformat_datetime_separator("2021-W12-")

    def test_find_isoformat_datetime_separator(self):
        separator = JalaliDateTime._find_isoformat_datetime_separator("1403-08-09T02:21:45")
        self.assertEqual(separator, 10)

    def test_parse_isoformat_time_with_microseconds(self):
        time_components = JalaliDateTime._parse_isoformat_time("02:21:45.123456")
        self.assertEqual(time_components, [2, 21, 45, 123456, None])

    def test_parse_isoformat_time_with_timezone(self):
        time_components = JalaliDateTime._parse_isoformat_time("02:21:45+04:30")
        self.assertEqual(time_components, [2, 21, 45, 0, timezone(timedelta(hours=4, minutes=30))])

    def test_parse_hh_mm_ss_ff_with_microseconds(self):
        time_components = JalaliDateTime._parse_hh_mm_ss_ff("02:21:45.123456")
        self.assertEqual(time_components, [2, 21, 45, 123456])

    def test_is_ascii_digit(self):
        self.assertTrue(_is_ascii_digit("5"))
        self.assertFalse(_is_ascii_digit("a"))

    def test_isoformat_round_trip(self):
        original = JalaliDateTime(1403, 8, 9, 2, 21, 45, 123456, tzinfo=timezone.utc)
        iso_format = original.isoformat()
        parsed = JalaliDateTime.fromisoformat(iso_format)
        self.assertEqual(original, parsed)

    def test_isoformat_timezone_representation(self):
        # 1. UTC Timezone
        jdt_utc = JalaliDateTime(1400, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(jdt_utc.isoformat(), "1400-01-01T12:00:00+00:00")

        # 2. Positive Offset Timezones
        tz_plus_3_30 = timezone(timedelta(hours=3, minutes=30))
        jdt_plus_3_30 = JalaliDateTime(1401, 2, 15, 10, 30, 0, tzinfo=tz_plus_3_30)
        self.assertEqual(jdt_plus_3_30.isoformat(), "1401-02-15T10:30:00+03:30")

        tz_plus_5 = timezone(timedelta(hours=5))
        jdt_plus_5 = JalaliDateTime(1402, 3, 20, 8, 0, 0, tzinfo=tz_plus_5)
        self.assertEqual(jdt_plus_5.isoformat(), "1402-03-20T08:00:00+05:00")

        # 3. Negative Offset Timezones
        tz_minus_4_45 = timezone(timedelta(hours=-4, minutes=-45))
        jdt_minus_4_45 = JalaliDateTime(1403, 4, 10, 16, 15, 0, tzinfo=tz_minus_4_45)
        self.assertEqual(jdt_minus_4_45.isoformat(), "1403-04-10T16:15:00-04:45")

        tz_minus_4_45 = timezone(timedelta(hours=-4, minutes=45))
        jdt_minus_4_45 = JalaliDateTime(1403, 4, 10, 16, 15, 0, tzinfo=tz_minus_4_45)
        self.assertEqual(jdt_minus_4_45.isoformat(), "1403-04-10T16:15:00-03:15")

        tz_direct_minus_4_45 = timezone(timedelta(seconds=-(4 * 3600 + 45 * 60)))
        jdt_direct_minus_4_45 = JalaliDateTime(1403, 4, 10, 16, 15, 0, tzinfo=tz_direct_minus_4_45)
        self.assertEqual(jdt_direct_minus_4_45.isoformat(), "1403-04-10T16:15:00-04:45")

        tz_minus_8 = timezone(timedelta(hours=-8))
        jdt_minus_8 = JalaliDateTime(1399, 12, 29, 23, 30, 59, tzinfo=tz_minus_8)
        self.assertEqual(jdt_minus_8.isoformat(), "1399-12-29T23:30:59-08:00")

        # 4. Offsets with zero minutes (covered by +05:00 and -08:00 above)
        self.assertEqual(
            JalaliDateTime(1402, 3, 20, 8, 0, 0, tzinfo=timezone(timedelta(hours=5))).isoformat(),
            "1402-03-20T08:00:00+05:00",
        )

        # 5. Microseconds with timezone offset
        jdt_utc_ms = JalaliDateTime(1400, 1, 1, 12, 30, 45, 123456, tzinfo=timezone.utc)
        self.assertEqual(jdt_utc_ms.isoformat(), "1400-01-01T12:30:45.123456+00:00")

        jdt_offset_ms = JalaliDateTime(1400, 6, 10, 10, 20, 30, 654321, tzinfo=tz_plus_3_30)
        self.assertEqual(jdt_offset_ms.isoformat(), "1400-06-10T10:20:30.654321+03:30")

        # 6. Default Separator 'T' (implicitly tested in all above cases)
        self.assertIn("T", jdt_utc.isoformat())

        # 7. Custom Separator
        jdt_custom_sep = JalaliDateTime(1400, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(jdt_custom_sep.isoformat(sep=" "), "1400-01-01 12:00:00+00:00")

        jdt_custom_sep_offset = JalaliDateTime(1401, 5, 5, 10, 10, 10, tzinfo=tz_minus_8)
        self.assertEqual(jdt_custom_sep_offset.isoformat(sep="_"), "1401-05-05_10:10:10-08:00")

        # 8. Naive JalaliDateTime (no offset string)
        jdt_naive = JalaliDateTime(1398, 10, 5, 12, 30, 0)
        self.assertEqual(jdt_naive.isoformat(), "1398-10-05T12:30:00")
        # With microseconds
        jdt_naive_ms = JalaliDateTime(1398, 10, 5, 12, 30, 0, 123)
        self.assertEqual(jdt_naive_ms.isoformat(), "1398-10-05T12:30:00.000123")
        # With custom separator
        self.assertEqual(jdt_naive.isoformat(sep=" "), "1398-10-05 12:30:00")
