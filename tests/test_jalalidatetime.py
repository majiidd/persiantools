import os
import pickle
import time
from datetime import date, datetime
from datetime import time as _time
from datetime import timedelta
from unittest import TestCase

import pytest
import pytz

from persiantools.jdatetime import JalaliDate, JalaliDateTime


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
            JalaliDateTime(1367, 2, 14, 4, 30, 0, 0),
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
        j = pickle.load(file2)
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
