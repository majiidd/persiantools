import os
import pickle
from datetime import date, timedelta
from time import struct_time, time
from unittest import TestCase

import pytest

from persiantools.jdatetime import MAXYEAR, MINYEAR, JalaliDate


class TestJalaliDate(TestCase):
    def test_shamsi_to_gregorian(self):
        cases = [
            (JalaliDate(1100, 1, 1), date(1721, 3, 21)),
            (JalaliDate(1210, 12, 30), date(1832, 3, 20)),
            (JalaliDate(1367, 2, 14), date(1988, 5, 4)),
            (JalaliDate(1395, 3, 21), date(2016, 6, 10)),
            (JalaliDate(1395, 12, 9), date(2017, 2, 27)),
            (JalaliDate(1400, 6, 31), date(2021, 9, 22)),
            (JalaliDate(1396, 7, 27), date(2017, 10, 19)),
            (JalaliDate(1397, 11, 29), date(2019, 2, 18)),
            (JalaliDate(1399, 10, 11), date(2020, 12, 31)),
            (JalaliDate(1399, 11, 23), date(2021, 2, 11)),
            (JalaliDate(1400, 4, 25), date(2021, 7, 16)),
            (JalaliDate(1400, 12, 20), date(2022, 3, 11)),
            (JalaliDate(1403, 1, 5), date(2024, 3, 24)),
            (JalaliDate(1402, 10, 10), date(2023, 12, 31)),
            (JalaliDate(1403, 10, 11), date(2024, 12, 31)),
            (JalaliDate(1403, 2, 23), date(2024, 5, 12)),
            (JalaliDate(1403, 4, 3), date(2024, 6, 23)),
            (JalaliDate(1403, 4, 8), date(2024, 6, 28)),
            (JalaliDate(1403, 8, 18), date(2024, 11, 8)),
            (JalaliDate(1404, 3, 16), date(2025, 6, 6)),
            (JalaliDate(1403, 10, 27), date(2025, 1, 16)),
            (JalaliDate(1210, 12, 29), date(1832, 3, 19)),
            (JalaliDate(1367, 12, 29), date(1989, 3, 20)),
            (JalaliDate(1392, 12, 29), date(2014, 3, 20)),
            (JalaliDate(1398, 12, 29), date(2020, 3, 19)),
            (JalaliDate(1399, 12, 29), date(2021, 3, 19)),
            (JalaliDate(1400, 12, 29), date(2022, 3, 20)),
            (JalaliDate(1402, 12, 29), date(2024, 3, 19)),
            (JalaliDate(1403, 12, 29), date(2025, 3, 19)),
            (JalaliDate(1504, 12, 29), date(2126, 3, 20)),
            (JalaliDate(1210, 12, 30), date(1832, 3, 20)),
            (JalaliDate(1391, 12, 30), date(2013, 3, 20)),
            (JalaliDate(1395, 12, 30), date(2017, 3, 20)),
            (JalaliDate(1399, 12, 30), date(2021, 3, 20)),
            (JalaliDate(1403, 12, 30), date(2025, 3, 20)),
            (JalaliDate(1408, 12, 30), date(2030, 3, 20)),
            (JalaliDate(1366, 10, 11), date(1988, 1, 1)),
            (JalaliDate(1378, 10, 11), date(2000, 1, 1)),
            (JalaliDate(1379, 10, 12), date(2001, 1, 1)),
            (JalaliDate(1390, 10, 11), date(2012, 1, 1)),
            (JalaliDate(1393, 10, 11), date(2015, 1, 1)),
            (JalaliDate(1398, 10, 11), date(2020, 1, 1)),
            (JalaliDate(1399, 10, 12), date(2021, 1, 1)),
            (JalaliDate(1400, 10, 11), date(2022, 1, 1)),
            (JalaliDate(1402, 10, 11), date(2024, 1, 1)),
            (JalaliDate(1403, 10, 12), date(2025, 1, 1)),
            (JalaliDate(1211, 1, 1), date(1832, 3, 21)),
            (JalaliDate(1367, 1, 1), date(1988, 3, 21)),
            (JalaliDate(1388, 1, 1), date(2009, 3, 21)),
            (JalaliDate(1396, 1, 1), date(2017, 3, 21)),
            (JalaliDate(1399, 1, 1), date(2020, 3, 20)),
            (JalaliDate(1400, 1, 1), date(2021, 3, 21)),
            (JalaliDate(1401, 1, 1), date(2022, 3, 21)),
            (JalaliDate(1402, 1, 1), date(2023, 3, 21)),
            (JalaliDate(1403, 1, 1), date(2024, 3, 20)),
            (JalaliDate(1404, 1, 1), date(2025, 3, 21)),
            (JalaliDate(1498, 12, 30), date(2120, 3, 20)),
            (JalaliDate(1505, 1, 1), date(2126, 3, 21)),
            (JalaliDate.today(), date.today()),
        ]
        for jdate, gdate in cases:
            self.assertEqual(jdate.to_gregorian(), gdate)

    def test_gregorian_to_shamsi(self):
        cases = [
            (date(1988, 5, 4), JalaliDate(1367, 2, 14)),
            (date(2122, 1, 31), JalaliDate(1500, 11, 11)),
            (date(2017, 10, 19), JalaliDate(1396, 7, 27)),
            (date(2019, 2, 18), JalaliDate(1397, 11, 29)),
            (date(1990, 9, 23), JalaliDate(1369, 7, 1)),
            (date(2013, 9, 16), JalaliDate(1392, 6, 25)),
            (date(2018, 3, 20), JalaliDate(1396, 12, 29)),
            (date(2021, 2, 11), JalaliDate(1399, 11, 23)),
            (date(2021, 7, 16), JalaliDate(1400, 4, 25)),
            (date(2024, 3, 24), JalaliDate(1403, 1, 5)),
            (date(2020, 3, 19), JalaliDate(1398, 12, 29)),
            (date(2024, 5, 12), JalaliDate(1403, 2, 23)),
            (date(2024, 6, 23), JalaliDate(1403, 4, 3)),
            (date(2000, 12, 31), JalaliDate(1379, 10, 11)),
            (date(2023, 12, 31), JalaliDate(1402, 10, 10)),
            (date(2024, 12, 31), JalaliDate(1403, 10, 11)),
            (date(1832, 3, 19), JalaliDate(1210, 12, 29)),
            (date(1832, 3, 20), JalaliDate(1210, 12, 30)),
            (date(2017, 3, 20), JalaliDate(1395, 12, 30)),
            (date(2021, 3, 20), JalaliDate(1399, 12, 30)),
            (date(2025, 3, 20), JalaliDate(1403, 12, 30)),
            (date(1832, 3, 21), JalaliDate(1211, 1, 1)),
            (date(2000, 1, 1), JalaliDate(1378, 10, 11)),
            (date(2012, 1, 1), JalaliDate(1390, 10, 11)),
            (date(2013, 1, 1), JalaliDate(1391, 10, 12)),
            (date(2020, 1, 1), JalaliDate(1398, 10, 11)),
            (date(2024, 1, 1), JalaliDate(1402, 10, 11)),
            (date(2025, 1, 1), JalaliDate(1403, 10, 12)),
            (date(1988, 3, 21), JalaliDate(1367, 1, 1)),
            (date(2009, 3, 21), JalaliDate(1388, 1, 1)),
            (date(2019, 3, 21), JalaliDate(1398, 1, 1)),
            (date(2020, 3, 20), JalaliDate(1399, 1, 1)),
            (date(2021, 3, 21), JalaliDate(1400, 1, 1)),
            (date(2023, 3, 21), JalaliDate(1402, 1, 1)),
            (date(2024, 3, 20), JalaliDate(1403, 1, 1)),
            (date(2025, 3, 21), JalaliDate(1404, 1, 1)),
            (date(1827, 3, 22), JalaliDate(1206, 1, 1)),
            (date(1828, 3, 21), JalaliDate(1207, 1, 1)),
            (date(1839, 3, 21), JalaliDate(1218, 1, 1)),
            (date(1864, 3, 20), JalaliDate(1243, 1, 1)),
            (date(2118, 3, 21), JalaliDate(1497, 1, 1)),
            (date(2119, 3, 21), JalaliDate(1498, 1, 1)),
            (date.today(), JalaliDate.today()),
        ]
        for gdate, jdate in cases:
            self.assertEqual(JalaliDate(gdate), jdate)

    def test_checkdate(self):
        cases = [
            (1206, 12, 30, False),
            (1210, 12, 30, True),
            (1214, 12, 30, True),
            (1367, 2, 14, True),
            (1395, 12, 30, True),
            (1394, 12, 30, False),
            (13, 13, 30, False),
            (0, 0, 0, False),
            (9378, 0, 0, False),
            ("1300", "1", "1", False),
            (1396, 12, 30, False),
            (1397, 7, 1, True),
            (1396, 7, 27, True),
            (1397, 11, 29, True),
            (1399, 11, 31, False),
            (1400, 1, 32, False),
            (1400, 4, 25, True),
            (1400, 12, 30, False),
            (1403, 4, 3, True),
            (1403, 12, 30, True),
            (1473, 12, 30, False),
            (1474, 12, 30, True),
            (1498, 12, 30, True),
        ]
        for year, month, day, valid in cases:
            self.assertEqual(JalaliDate.check_date(year, month, day), valid)

        with pytest.raises(ValueError):
            JalaliDate._check_date_fields(1404, 3, 16, "ar")

    def test_completeday(self):
        jdate = JalaliDate(1398, 3, 17)
        self.assertEqual(jdate.year, 1398)
        self.assertEqual(jdate.month, 3)
        self.assertEqual(jdate.day, 17)
        self.assertEqual(jdate.locale, "en")
        self.assertEqual(jdate.to_gregorian(), date(2019, 6, 7))
        self.assertEqual(jdate.isoformat(), "1398-03-17")
        self.assertEqual(jdate.weekday(), 6)
        self.assertEqual(jdate.isoweekday(), 7)
        self.assertEqual(jdate.week_of_year(), 12)
        self.assertEqual(jdate.isocalendar(), (1398, 12, 7))
        self.assertEqual(jdate.ctime(), "Jomeh 17 Khordad 1398")
        self.assertEqual(jdate - JalaliDate(1398, 1, 1), timedelta(days=78))
        self.assertEqual(jdate > JalaliDate(1398, 3, 16), True)
        self.assertEqual(JalaliDate(1398, 3, 16) + timedelta(days=1), jdate)
        self.assertEqual(jdate.timetuple(), struct_time((2019, 6, 7, 0, 0, 0, 4, 158, -1)))

        jdate = JalaliDate(1399, 11, 23)
        self.assertEqual(jdate.to_gregorian(), date(2021, 2, 11))
        self.assertEqual(jdate.isoformat(), "1399-11-23")
        self.assertEqual(jdate.weekday(), 5)
        self.assertEqual(jdate.week_of_year(), 48)

    def test_timetuple(self):
        cases = [
            (JalaliDate(1398, 3, 17), struct_time((2019, 6, 7, 0, 0, 0, 4, 158, -1))),
            (JalaliDate(1367, 2, 14), struct_time((1988, 5, 4, 0, 0, 0, 2, 125, -1))),
        ]
        for jdate, ttuple in cases:
            self.assertEqual(jdate.timetuple(), ttuple)

    def test_isocalendar(self):
        cases = [
            (JalaliDate(1364, 1, 31), (1364, 6, 1)),
            (JalaliDate(1398, 3, 17), (1398, 12, 7)),
            (JalaliDate(1398, 1, 1), (1398, 1, 6)),
            (JalaliDate(1399, 1, 2), (1399, 2, 1)),
            (JalaliDate(1403, 1, 5), (1403, 2, 2)),
        ]
        for jdate, iso in cases:
            self.assertEqual(jdate.isocalendar(), iso)

    def test_additions(self):
        self.assertEqual(JalaliDate(JalaliDate(1395, 3, 21)), JalaliDate(1395, 3, 21))
        self.assertEqual(JalaliDate.days_before_month(1), 0)
        self.assertEqual(JalaliDate.days_before_month(12), 336)

        self.assertEqual(JalaliDate(1395, 1, 1).replace(1367), JalaliDate(1367, 1, 1))
        self.assertEqual(JalaliDate(1395, 1, 1).replace(month=2), JalaliDate(1395, 2, 1))
        self.assertEqual(JalaliDate(1367, 1, 1).replace(year=1396, month=7), JalaliDate(1396, 7, 1))
        self.assertEqual(
            JalaliDate(1395, 1, 1, "en").replace(1367, 2, 14, "fa"),
            JalaliDate(1367, 2, 14, "en"),
        )

        self.assertEqual(JalaliDate.fromtimestamp(time()), JalaliDate.today())
        self.assertEqual(JalaliDate.fromtimestamp(578707200), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate.fromtimestamp(1508371200), JalaliDate(1396, 7, 27))

        with pytest.raises(ValueError):
            JalaliDate(1400, 1, 1, "us")

        jdate = JalaliDate.today()
        with pytest.raises(ValueError, match="locale must be 'en' or 'fa'"):
            jdate.replace(locale="de")

        with pytest.raises(ValueError):
            JalaliDate.days_before_month(0)

        with pytest.raises(ValueError):
            JalaliDate.days_before_month(13)

        with pytest.raises(ValueError):
            JalaliDate.days_in_month(13, 1404)

        with pytest.raises(ValueError):
            JalaliDate.days_in_month(0, 1400)

    def test_leap(self):
        cases = [
            # First 33-year cycle
            (1210, True),
            (1214, True),
            (1218, True),
            (1222, True),
            (1226, True),
            (1230, True),
            (1234, True),
            (1238, True),
            (1243, True),  # 33-year marker
            # Second 33-year cycle
            (1247, True),
            (1251, True),
            (1255, True),
            (1259, True),
            (1263, True),
            (1267, True),
            (1271, True),
            (1276, True),  # 33-year marker
            (1280, True),
            (1284, True),
            (1288, True),
            (1292, True),
            (1296, True),
            (1300, True),
            (1304, True),
            (1309, True),  # 33-year marker
            (1313, True),
            (1317, True),
            (1321, True),
            (1325, True),
            (1329, True),
            (1333, True),
            (1337, True),
            (1342, True),  # 33-year marker
            (1346, True),
            (1350, True),
            (1354, True),
            (1358, True),
            (1362, True),
            (1366, True),
            (1370, True),
            (1375, True),  # 33-year marker
            (1379, True),
            (1383, True),
            (1387, True),
            (1391, True),
            (1395, True),
            (1399, True),
            (1403, True),
            (1408, True),  # 33-year marker
            (1412, True),
            (1416, True),
            (1420, True),
            (1424, True),
            (1428, True),
            (1432, True),
            (1436, True),
            (1441, True),  # 33-year marker
            (1445, True),
            (1449, True),
            (1453, True),
            (1457, True),
            (1461, True),
            (1465, True),
            (1469, True),
            (1474, True),  # 33-year marker
            (1478, True),
            (1482, True),
            (1486, True),
            (1490, True),
            (1494, True),
            (1498, True),
            # Known non-leap years
            (1206, False),
            (1207, False),
            (1208, False),
            (1209, False),
            (1211, False),
            (1215, False),
            (1216, False),
            (1219, False),
            (1223, False),
            (1227, False),
            (1231, False),
            (1235, False),
            (1239, False),
            (1367, False),
            (1396, False),
            (1397, False),
            (1398, False),
            (1400, False),
            (1401, False),
            (1402, False),
            (1404, False),
            (1405, False),
            (1406, False),
            (1407, False),
            (1409, False),
            (1410, False),
            (1411, False),
            (1493, False),
            (1495, False),
            (1496, False),
            (1497, False),
        ]
        for year, is_leap in cases:
            self.assertEqual(JalaliDate.is_leap(year), is_leap)

        invalid_year_below = MINYEAR - 1
        invalid_year_above = MAXYEAR + 1

        with pytest.raises(ValueError, match=f"Year must be between {MINYEAR} and {MAXYEAR}"):
            JalaliDate.is_leap(invalid_year_below)

        with pytest.raises(ValueError, match=f"Year must be between {MINYEAR} and {MAXYEAR}"):
            JalaliDate.is_leap(invalid_year_above)

    def test_format(self):
        j = JalaliDate(date(1988, 5, 4))
        self.assertEqual(j.isoformat(), "1367-02-14")
        self.assertEqual(j.strftime("%a %A %w"), "Cha Chaharshanbeh 4")

        j.locale = "fa"

        self.assertEqual(j.isoformat(), "۱۳۶۷-۰۲-۱۴")
        self.assertEqual(j.strftime("%a %A %w"), "چ چهارشنبه ۴")

        j = JalaliDate(1395, 3, 1)

        self.assertEqual(j.strftime("%d %b %B"), "01 Kho Khordad")
        self.assertEqual(j.strftime("%m %m %y %Y"), "03 03 95 1395")
        self.assertEqual(j.strftime("%p %j %j %U %W %%"), "AM 063 063 10 10 %")
        self.assertEqual(j.strftime("%c"), j.ctime())
        self.assertEqual(j.strftime("%c"), "Shanbeh 01 Khordad 1395")
        self.assertEqual(j.strftime("%x"), "95/03/01")
        self.assertEqual(format(j, "%c"), j.ctime())
        self.assertEqual(format(j), "1395-03-01")
        self.assertEqual(j.__repr__(), "JalaliDate(1395, 3, 1, Shanbeh)")

        j.locale = "fa"

        self.assertEqual(j.strftime("%d %b %B"), "۰۱ خرد خرداد")
        self.assertEqual(j.strftime("%m %m %y %Y"), "۰۳ ۰۳ ۹۵ ۱۳۹۵")
        self.assertEqual(j.strftime("%p %j %j %U %W %%"), "ق.ظ ۰۶۳ ۰۶۳ ۱۰ ۱۰ %")
        self.assertEqual(j.strftime("%c"), j.ctime())
        self.assertEqual(j.strftime("%c"), "شنبه ۰۱ خرداد ۱۳۹۵")
        self.assertEqual(j.strftime("%x"), "۹۵/۰۳/۰۱")
        self.assertEqual(format(j, "%c"), j.ctime())
        self.assertEqual(j.__repr__(), "JalaliDate(1395, 3, 1, Shanbeh)")

        self.assertEqual(format(j), "۱۳۹۵-۰۳-۰۱")

        with pytest.raises(TypeError):
            format(j, 1)

        j = JalaliDate(1397, 11, 29)

        self.assertEqual(j.strftime("%c"), "Doshanbeh 29 Bahman 1397")
        self.assertEqual(format(j), "1397-11-29")

        j.locale = "fa"

        self.assertEqual(j.strftime("%c"), "دوشنبه ۲۹ بهمن ۱۳۹۷")
        self.assertEqual(format(j), "۱۳۹۷-۱۱-۲۹")

        j = JalaliDate(1400, 4, 25)
        self.assertEqual(j.strftime("%c", "fa"), "جمعه ۲۵ تیر ۱۴۰۰")

        self.assertEqual(JalaliDate(1367, 2, 14), JalaliDate.fromisoformat("1367-02-14"))
        self.assertEqual(JalaliDate(1397, 12, 9), JalaliDate.fromisoformat("۱۳۹۷-۱۲-۰۹"))

        with pytest.raises(TypeError):
            JalaliDate.fromisoformat(13670214)

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1367/02/14")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1367-02/14")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("2021-W1")

        with pytest.raises(ValueError, match="Invalid isoformat string: '2021-W12-'"):
            JalaliDate.fromisoformat("2021-W12-")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("2021-W12-34")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("2021W12-X")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("2021W123")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1395-03")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("13950301")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1395-13-01")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1400-01-32")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1395-03-01 extra")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat(" 1395-03-01")

        j_date = JalaliDate(1400, 1, 1)
        self.assertEqual(j_date.strftime("%A, %d %B %Y"), "Yekshanbeh, 01 Farvardin 1400")
        self.assertEqual(j_date.strftime("%A, %d %B %Y", locale="fa"), "یکشنبه, ۰۱ فروردین ۱۴۰۰")

    def test_week(self):
        self.assertEqual(JalaliDate(1394, 3, 30).week_of_year(), 14)
        self.assertEqual(JalaliDate(1394, 7, 30).week_of_year(), 31)
        self.assertEqual(JalaliDate(1394, 10, 11).week_of_year(), 41)
        self.assertEqual(JalaliDate(1394, 12, 29).week_of_year(), 53)
        self.assertEqual(JalaliDate(1395, 1, 21).week_of_year(), 4)
        self.assertEqual(JalaliDate(1395, 3, 21).week_of_year(), 12)
        self.assertEqual(JalaliDate(1395, 7, 1).week_of_year(), 27)
        self.assertEqual(JalaliDate(1395, 12, 27).week_of_year(), 52)
        self.assertEqual(JalaliDate(1395, 12, 30).week_of_year(), 53)
        self.assertEqual(JalaliDate(1396, 1, 25).week_of_year(), 4)
        self.assertEqual(JalaliDate(1396, 7, 8).week_of_year(), 29)
        self.assertEqual(JalaliDate(1397, 11, 29).week_of_year(), 49)
        self.assertEqual(JalaliDate(1399, 1, 2).week_of_year(), 2)
        self.assertEqual(JalaliDate(1403, 1, 5).week_of_year(), 2)
        self.assertEqual(JalaliDate(1403, 4, 3).week_of_year(), 15)
        self.assertEqual(JalaliDate(1403, 10, 28).week_of_year(), 44)

        self.assertEqual(JalaliDate(1367, 2, 14).weekday(), 4)
        self.assertEqual(JalaliDate(1393, 1, 1).weekday(), 6)
        self.assertEqual(JalaliDate(1394, 1, 1).weekday(), 0)
        self.assertEqual(JalaliDate(1394, 1, 1).isoweekday(), 1)
        self.assertEqual(JalaliDate(1395, 1, 1).weekday(), 1)
        self.assertEqual(JalaliDate(1395, 3, 21).weekday(), 6)
        self.assertEqual(JalaliDate(1396, 1, 1).weekday(), 3)
        self.assertEqual(JalaliDate(1396, 7, 27).weekday(), 5)
        self.assertEqual(JalaliDate(1397, 1, 1).weekday(), 4)
        self.assertEqual(JalaliDate(1397, 11, 29).weekday(), 2)
        self.assertEqual(JalaliDate(1400, 1, 1).weekday(), 1)
        self.assertEqual(JalaliDate(1403, 10, 28).weekday(), 6)

        self.assertEqual(JalaliDate(1403, 4, 3).isoweekday(), 2)
        self.assertEqual(JalaliDate(1400, 1, 1).isoweekday(), 2)
        self.assertEqual(JalaliDate(1396, 7, 27).isoweekday(), 6)
        self.assertEqual(JalaliDate(1397, 11, 29).isoweekday(), 3)
        self.assertEqual(JalaliDate(1403, 10, 28).isoweekday(), 7)

    def test_operators(self):
        self.assertTrue(JalaliDate(1367, 2, 14) == JalaliDate(date(1988, 5, 4)))
        self.assertTrue(JalaliDate(1367, 2, 14) == date(1988, 5, 4), True)
        self.assertTrue(JalaliDate(1396, 7, 27) == JalaliDate(date(2017, 10, 19)))
        self.assertFalse(JalaliDate(1367, 2, 14) != JalaliDate(date(1988, 5, 4)))
        self.assertFalse(JalaliDate(1367, 2, 14) != date(1988, 5, 4))
        self.assertTrue(JalaliDate(1367, 2, 14) < JalaliDate(1369, 1, 1))
        self.assertFalse(JalaliDate(1367, 2, 14) < date(1988, 5, 4))
        self.assertTrue(JalaliDate(1395, 12, 30) > JalaliDate(1395, 12, 29))
        self.assertTrue(JalaliDate(1395, 12, 30) > date(2000, 11, 15))
        self.assertTrue(JalaliDate(1395, 12, 30) >= JalaliDate(1395, 12, 30))
        self.assertFalse(JalaliDate(1367, 2, 13) >= date(1988, 5, 4))
        self.assertTrue(JalaliDate(1367, 2, 14) <= JalaliDate(1369, 1, 1))
        self.assertTrue(JalaliDate(1367, 2, 14) <= date(1988, 5, 4))
        self.assertFalse(JalaliDate(1367, 2, 14) >= JalaliDate(1369, 1, 1))
        self.assertTrue(JalaliDate(1397, 11, 29) >= JalaliDate(1397, 11, 10))
        self.assertTrue(JalaliDate(1399, 12, 30) > JalaliDate(1399, 12, 29))
        self.assertTrue(JalaliDate(1399, 12, 29) < JalaliDate(1400, 1, 1))
        self.assertTrue(JalaliDate(1400, 1, 1) == JalaliDate(1400, 1, 1))
        self.assertFalse(JalaliDate(1399, 12, 30) == JalaliDate(1400, 1, 1))
        self.assertTrue(JalaliDate(1403, 12, 30) > JalaliDate(1403, 12, 29))
        self.assertTrue(JalaliDate(1404, 1, 1) > JalaliDate(1403, 12, 30))

        self.assertFalse(JalaliDate(1367, 2, 14) == (1367, 2, 14))
        self.assertFalse(JalaliDate(1367, 2, 14) == "")
        self.assertTrue(JalaliDate(1367, 2, 14) != 5)

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) < "string"

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) <= 0.5

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) > True

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) >= [1367, 2, 14]

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) + b"A"

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) - {1, 2}

    def test_arithmetic_operations(self):
        self.assertEqual(JalaliDate(1395, 3, 21) + timedelta(days=2), JalaliDate(1395, 3, 23))
        self.assertEqual(JalaliDate(1396, 7, 27) + timedelta(days=4), JalaliDate(1396, 8, 1))
        self.assertEqual(JalaliDate(1395, 3, 21) + timedelta(days=-38), JalaliDate(1395, 2, 14))
        self.assertEqual(JalaliDate(1395, 3, 21) - timedelta(days=38), JalaliDate(1395, 2, 14))
        self.assertEqual(JalaliDate(1397, 11, 29) + timedelta(days=2), JalaliDate(1397, 12, 1))
        self.assertEqual(JalaliDate(1403, 12, 29) + timedelta(days=2), JalaliDate(1404, 1, 1))
        self.assertEqual(JalaliDate(1403, 12, 29) + timedelta(days=365), JalaliDate(1404, 12, 28))

        self.assertEqual(JalaliDate(1395, 3, 21) - JalaliDate(1395, 2, 14), timedelta(days=38))
        self.assertEqual(JalaliDate(1397, 12, 1) - JalaliDate(1397, 11, 29), timedelta(hours=48))
        self.assertEqual(JalaliDate(1395, 3, 21) - date(2016, 5, 3), timedelta(days=38))
        self.assertEqual(JalaliDate(1395, 12, 30) - JalaliDate(1395, 1, 1), timedelta(days=365))
        self.assertEqual(JalaliDate(1399, 1, 1) - JalaliDate(1398, 1, 1), timedelta(days=365))
        self.assertEqual(JalaliDate(1399, 12, 29) + timedelta(days=2), JalaliDate(1400, 1, 1))
        self.assertEqual(JalaliDate(1400, 1, 1) - timedelta(days=1), JalaliDate(1399, 12, 30))
        self.assertEqual(JalaliDate(1400, 1, 1) - JalaliDate(1399, 12, 29), timedelta(days=2))
        self.assertEqual(JalaliDate(1403, 1, 1) - JalaliDate(1402, 12, 29), timedelta(days=1))
        self.assertEqual(JalaliDate(1404, 1, 1) - JalaliDate(1403, 12, 29), timedelta(days=2))
        self.assertEqual(JalaliDate(1404, 1, 1) - JalaliDate(1403, 12, 30), timedelta(days=1))

    def test_pickle(self):
        file = open("save.p", "wb")
        pickle.dump(JalaliDate(1367, 2, 14), file, protocol=2)
        file.close()

        file2 = open("save.p", "rb")
        j = pickle.load(file2)  # nosec B301
        file2.close()

        self.assertEqual(j, JalaliDate(1367, 2, 14))

        os.remove("save.p")

    def test_hash(self):
        j1 = JalaliDate.today()
        j2 = JalaliDate(1367, 2, 14)
        j3 = JalaliDate(date(1988, 5, 4))

        self.assertEqual(
            {j1: "today", j2: "majid1", j3: "majid2"},
            {JalaliDate.today(): "today", JalaliDate(date(1988, 5, 4)): "majid1", JalaliDate(1367, 2, 14): "majid2"},
        )

    def test_invalid_dates(self):
        with self.assertRaises(ValueError):
            JalaliDate(1403, 13, 1)
        with self.assertRaises(ValueError):
            JalaliDate(1403, 1, 32)
        with self.assertRaises(ValueError):
            JalaliDate(1403, -1, 1)

    def test_round_trip_conversion(self):
        jdate = JalaliDate(1399, 12, 30)
        gdate = jdate.to_gregorian()
        self.assertEqual(JalaliDate.to_jalali(gdate), jdate)

        gdate = date(2021, 3, 20)
        jdate = JalaliDate.to_jalali(gdate)
        self.assertEqual(jdate.to_gregorian(), gdate)

    def test_string_representation(self):
        self.assertEqual(str(JalaliDate(1403, 4, 7)), "1403-04-07")
        self.assertEqual(repr(JalaliDate(1403, 4, 7)), "JalaliDate(1403, 4, 7, Panjshanbeh)")

    def test_strptime(self):
        # 1. Basic parsing
        self.assertEqual(JalaliDate.strptime("1367-02-14", "%Y-%m-%d"), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate.strptime("1367/02/14", "%Y/%m/%d"), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate.strptime("13670214", "%Y%m%d"), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate.strptime("16/03/1404", "%d/%m/%Y"), JalaliDate(1404, 3, 16))
        self.assertEqual(JalaliDate.strptime("16/03/1404", "%d/%m/%Y", locale="en"), JalaliDate(1404, 3, 16))

        # 2. Year variations
        self.assertEqual(JalaliDate.strptime("99-01-01", "%y-%m-%d"), JalaliDate(1399, 1, 1))  # 99 > 70 => 1399
        self.assertEqual(JalaliDate.strptime("00-01-01", "%y-%m-%d"), JalaliDate(1400, 1, 1))
        self.assertEqual(JalaliDate.strptime("01-01-01", "%y-%m-%d"), JalaliDate(1401, 1, 1))  # 01 <= 70 => 1401
        self.assertEqual(JalaliDate.strptime("04-01-01", "%y-%m-%d"), JalaliDate(1404, 1, 1))
        self.assertEqual(JalaliDate.strptime("70-10-10", "%y-%m-%d"), JalaliDate(1470, 10, 10))  # 70 => 1470

        # 3. Month variations
        self.assertEqual(JalaliDate.strptime("1400-01-15", "%Y-%m-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1400-Far-15", "%Y-%b-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1400-FAR-15", "%Y-%b-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1400-far-15", "%Y-%b-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1367-Ord-14", "%Y-%b-%d"), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate.strptime("1400-Farvardin-15", "%Y-%B-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1400-FARVARDIN-15", "%Y-%B-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1400-farvardin-15", "%Y-%B-%d"), JalaliDate(1400, 1, 15))
        self.assertEqual(JalaliDate.strptime("1400-Ordibehesht-10", "%Y-%B-%d"), JalaliDate(1400, 2, 10))
        self.assertEqual(JalaliDate.strptime("1398-Esf-05", "%Y-%b-%d"), JalaliDate(1398, 12, 5))
        self.assertEqual(JalaliDate.strptime("1403-Esfand-30", "%Y-%B-%d"), JalaliDate(1403, 12, 30))

        # 4. Day variations
        self.assertEqual(JalaliDate.strptime("1404-03-05", "%Y-%m-%d"), JalaliDate(1404, 3, 5))
        self.assertEqual(JalaliDate.strptime("1404-03-31", "%Y-%m-%d"), JalaliDate(1404, 3, 31))

        # 5. Locale testing ('en' and 'fa')
        self.assertEqual(
            JalaliDate.strptime("1401-Ord-05", "%Y-%b-%d", locale="en"), JalaliDate(1401, 2, 5, locale="en")
        )

        # Persian locale
        self.assertEqual(
            JalaliDate.strptime("۱۴۰۰-۰۱-۱۵", "%Y-%m-%d", locale="fa"), JalaliDate(1400, 1, 15, locale="fa")
        )
        self.assertEqual(
            JalaliDate.strptime("۱۴۰۰-فروردین-۱۵", "%Y-%B-%d", locale="fa"), JalaliDate(1400, 1, 15, locale="fa")
        )
        self.assertEqual(
            JalaliDate.strptime("۱۴۰۰-فرو-۱۵", "%Y-%b-%d", locale="fa"), JalaliDate(1400, 1, 15, locale="fa")
        )
        self.assertEqual(
            JalaliDate.strptime("۱۴۰۰-اردیبهشت-۱۰", "%Y-%B-%d", locale="fa"), JalaliDate(1400, 2, 10, locale="fa")
        )
        self.assertEqual(
            JalaliDate.strptime("۱۳۹۸-اسفند-۰۵", "%Y-%B-%d", locale="fa"), JalaliDate(1398, 12, 5, locale="fa")
        )
        self.assertEqual(
            JalaliDate.strptime("۱۳۹۸-اسف-۰۵", "%Y-%b-%d", locale="fa"), JalaliDate(1398, 12, 5, locale="fa")
        )
        # Mixed Farsi digits and names
        self.assertEqual(
            JalaliDate.strptime("1398-اسفند-۰۵", "%Y-%B-%d", locale="fa"), JalaliDate(1398, 12, 5, locale="fa")
        )

        # 6. Format strings with literals and different separators
        self.assertEqual(JalaliDate.strptime("Date: 1404/12 Day: 29", "Date: %Y/%m Day: %d"), JalaliDate(1404, 12, 29))
        self.assertEqual(
            JalaliDate.strptime("Year 1367 Month 02 Day 14", "Year %Y Month %m Day %d"), JalaliDate(1367, 2, 14)
        )
        # self.assertEqual(JalaliDate.strptime("1400|01|01", "%Y|%m|%d"), JalaliDate(1400, 1, 1))
        self.assertEqual(JalaliDate.strptime("Jalali:1403-10-20", "Jalali:%Y-%m-%d"), JalaliDate(1403, 10, 20))

        # 7. Weekday directives (%a and %A) - parsed but ignored for date construction
        self.assertEqual(
            JalaliDate.strptime("Jomeh, 1404-03-16", "%A, %Y-%m-%d"), JalaliDate(1404, 3, 16)
        )  # 1404-03-16 is a Jomeh
        self.assertEqual(JalaliDate.strptime("Sha, 1400-01-06", "%a, %Y-%m-%d"), JalaliDate(1400, 1, 6))
        self.assertEqual(JalaliDate.strptime("Yekshanbeh 1400-Farvardin-01", "%A %Y-%B-%d"), JalaliDate(1400, 1, 1))
        # Test with fa locale weekdays
        self.assertEqual(
            JalaliDate.strptime("شنبه, ۱۴۰۰-۰۱-۰۶", "%A, %Y-%m-%d", locale="fa"), JalaliDate(1400, 1, 6, locale="fa")
        )
        self.assertEqual(
            JalaliDate.strptime("ش, ۱۴۰۰-۰۱-۰۶", "%a, %Y-%m-%d", locale="fa"), JalaliDate(1400, 1, 6, locale="fa")
        )

        # 8. Invalid inputs
        with self.assertRaises(ValueError, msg="Month out of range"):
            JalaliDate.strptime("1400-13-01", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Day out of range for month"):
            JalaliDate.strptime("1400-01-32", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Day out of range for month (Mehr has 30 days)"):
            JalaliDate.strptime("1400-07-31", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Invalid month name"):
            JalaliDate.strptime("1399/Feb/20", "%Y/%b/%d")
        with self.assertRaises(ValueError, msg="String does not match format"):
            JalaliDate.strptime("1400/01/01 Extra", "%Y/%m/%d")
        with self.assertRaises(ValueError, msg="String does not match format - incorrect separator"):
            JalaliDate.strptime("1400.01.01", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Year with %Y must be 4 digits"):
            JalaliDate.strptime("123-01-01", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Year with %y must be 2 digits"):  # The regex for %y is \d{2}
            JalaliDate.strptime("1-01-01", "%y-%m-%d")
        with self.assertRaises(ValueError, msg="Date string does not match format (empty date string)"):
            JalaliDate.strptime("", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Date string does not match format (empty format string)"):
            JalaliDate.strptime("1400-01-01", "")
        with self.assertRaises(ValueError, msg="Month information missing"):
            JalaliDate.strptime("1400--01", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Day information missing"):
            JalaliDate.strptime("1400-01-", "%Y-%m-%d")
        with self.assertRaises(ValueError, msg="Year information missing"):
            JalaliDate.strptime("-01-01", "%Y-%m-%d")
        with self.assertRaises(ValueError):
            JalaliDate.strptime("1402-12-30", "%Y-%m-%d")
        with self.assertRaises(ValueError):
            JalaliDate.strptime("98-12-30", "%y-%m-%d")
        with self.assertRaises(ValueError):
            JalaliDate.strptime("1404-01-01", "%Y-%m-%d", "ar")

        # 9. Edge cases
        # Leap year: 1399 was a leap year (Esfand has 30 days)
        self.assertEqual(JalaliDate.strptime("1399-12-30", "%Y-%m-%d"), JalaliDate(1399, 12, 30))
        # Non-leap year: 1400 was not a leap year (Esfand has 29 days)
        self.assertEqual(JalaliDate.strptime("1400-12-29", "%Y-%m-%d"), JalaliDate(1400, 12, 29))
        with self.assertRaises(ValueError, msg="Esfand 30 on non-leap year 1400"):
            JalaliDate.strptime("1400-12-30", "%Y-%m-%d")

        # Leap year: 1403 is a leap year
        self.assertEqual(JalaliDate.strptime("1403-12-30", "%Y-%m-%d"), JalaliDate(1403, 12, 30))
        self.assertEqual(JalaliDate.strptime("03-12-30", "%y-%m-%d"), JalaliDate(1403, 12, 30))

        self.assertEqual(JalaliDate.strptime(f"{MINYEAR:04d}-01-01", "%Y-%m-%d"), JalaliDate(MINYEAR, 1, 1))
        self.assertEqual(JalaliDate.strptime(f"{MAXYEAR:04d}-12-29", "%Y-%m-%d"), JalaliDate(MAXYEAR, 12, 29))

        # Test %x and %c replacements
        # %x: %Y/%m/%d
        self.assertEqual(JalaliDate.strptime("1399/05/10", "%x"), JalaliDate(1399, 5, 10))
        # %c: %a %b %d %Y
        self.assertEqual(JalaliDate.strptime("Sha Far 01 1380", "%c"), JalaliDate(1380, 1, 1))  # 1380-01-01 is Shanbeh
        self.assertEqual(JalaliDate.strptime("ش فرو ۰۱ ۱۳۸۰", "%c", locale="fa"), JalaliDate(1380, 1, 1, locale="fa"))

        self.assertEqual(JalaliDate.strptime("1400-Tir-15", "%Y-%b-%d"), JalaliDate(1400, 4, 15))

    def test_locale_setter_invalid_value(self):
        jdate = JalaliDate.today()

        with pytest.raises(ValueError, match="locale must be 'en' or 'fa'"):
            jdate.locale = "de"

    def test_setstate(self):
        jdate = JalaliDate(1400, 1, 1)
        state = bytes([5, 87, 2, 14])
        jdate.__setstate__(state)

        self.assertEqual(jdate.year, 1367)
        self.assertEqual(jdate.month, 2)
        self.assertEqual(jdate.day, 14)

        jdate = JalaliDate(1400, 1, 1)
        state = bytes([5, 112, 1])  # Invalid length
        with pytest.raises(TypeError, match="not enough arguments"):
            jdate.__setstate__(state)
