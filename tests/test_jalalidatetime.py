# -*- coding: utf-8 -*-
import time
from datetime import datetime, date, timedelta
from unittest import TestCase

import pytz

from persiantools.jdatetime import JalaliDateTime, JalaliDate


class TestJalaliDate(TestCase):
    def test_base(self):
        self.assertEqual(JalaliDateTime(1367, 2, 14, 14, 0, 0, 0),
                         JalaliDateTime.to_jalali(datetime(1988, 5, 4, 14, 0, 0, 0)))
        self.assertEqual(JalaliDateTime(1369, 7, 1, 14, 14, 1, 1111),
                         JalaliDateTime(datetime(1990, 9, 23, 14, 14, 1, 1111)))
        self.assertEqual(JalaliDateTime(1369, 7, 1, 14, 14, 1, 9111),
                         JalaliDateTime(JalaliDateTime(1369, 7, 1, 14, 14, 1, 9111)))

    def test_others(self):
        self.assertTrue(JalaliDateTime.fromtimestamp(time.time()) <= JalaliDateTime.now())
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc).timestamp(), 578723400)
        self.assertEqual(JalaliDateTime.fromtimestamp(578710800), JalaliDateTime(1367, 2, 14, 4, 30, 0, 0))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).jdate(), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).date(), date(1988, 5, 4))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).__repr__(), 'JalaliDateTime(1367, 2, 14, 4, 30)')
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).replace(year=1395, day=3, minute=59),
                         JalaliDateTime(1395, 2, 3, 4, 59, 4, 4444))

        self.assertEqual(JalaliDateTime.now(pytz.utc).tzname(), "UTC")
        self.assertEqual(JalaliDateTime.now(pytz.timezone("Asia/Tehran")).replace(month=2).dst(), timedelta(hours=1))
        self.assertIsNone(JalaliDateTime.today().tzname())
        self.assertIsNone(JalaliDateTime.today().dst())

        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).ctime(), "Chaharshanbeh 14 Ordibehesht 1367 04:30:00")
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).replace(locale="fa").ctime(),
                         "چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۰۴:۳۰:۰۰")

        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 1, pytz.utc).isoformat(),
                         "1367-02-14T04:30:00.000001+00:00")
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 1, pytz.utc).__str__(),
                         "1367-02-14 04:30:00.000001+00:00")

    def test_operators(self):
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) + timedelta(days=30, seconds=15, milliseconds=1),
                         JalaliDateTime(1367, 3, 13, 4, 30, 15, 1000))
        self.assertEqual(JalaliDateTime(1395, 2, 14, 4, 30, 0, 0) - JalaliDateTime(1367, 2, 14, 4, 30, 0, 0),
                         timedelta(days=10226))
        self.assertEqual(JalaliDateTime(1395, 4, 16, 20, 14, 30, 0) - timedelta(days=1, seconds=31),
                         JalaliDateTime(1395, 4, 15, 20, 13, 59, 0))

        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) < JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertTrue(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) <= JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) > JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertFalse(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0) >= JalaliDateTime(1369, 7, 1, 1, 0, 0, 0))
        self.assertTrue(JalaliDateTime(1395, 4, 15, 20, 13, 59, 0) == JalaliDateTime(1395, 4, 15, 20, 13, 59, 0))
        self.assertTrue(
            JalaliDateTime(1395, 4, 15, 20, 13, 59, 0, pytz.utc) != JalaliDateTime(1395, 4, 15, 20, 13, 59, 0))
        self.assertTrue(JalaliDateTime.now() != JalaliDateTime.now())

        self.assertEqual(
            JalaliDateTime(1395, 4, 16, 20, 14, 30, 0, pytz.utc) - JalaliDateTime(1395, 4, 16, 20, 14, 30, 0,
                                                                                  pytz.timezone("Asia/Tehran")),
            pytz.timezone("Asia/Tehran")._utcoffset)

    def test_hash(self):
        j1 = JalaliDateTime.today().replace(tzinfo=pytz.utc)
        j2 = JalaliDateTime(1369, 7, 1, 0, 0, 0, 0)
        j3 = JalaliDateTime(datetime(1990, 9, 23, 0, 0, 0, 0))

        self.assertEqual({j1: "today", j2: "mini1", j3: "mini2"},
                         {JalaliDateTime(j1.year, j1.month, j1.day, j1.hour, j1.minute, j1.second,
                                         j1.microsecond, j1.tzinfo): "today",
                          JalaliDateTime(1369, 7, 1, 0, 0, 0, 0): "mini2"})
