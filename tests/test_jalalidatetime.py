# -*- coding: utf-8 -*-
import os
import pickle
import time
from datetime import datetime, date, timedelta, time as _time, tzinfo
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

        g = JalaliDateTime.now()
        self.assertEqual(g.time(), _time(g.hour, g.minute, g.second, g.microsecond))

        g = g.replace(tzinfo=pytz.timezone("America/Los_Angeles"))
        self.assertEqual(g.timetz(),
                         _time(g.hour, g.minute, g.second, g.microsecond, pytz.timezone("America/Los_Angeles")))

        self.assertEqual(JalaliDateTime.fromtimestamp(578723400, pytz.utc),
                         JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc))
        self.assertEqual(JalaliDateTime.utcfromtimestamp(578723400), JalaliDateTime(1367, 2, 14, 4, 30, 0, 0))

        try:
            JalaliDateTime._check_time_fields(20, 1, 61, 1000)
        except ValueError:
            assert True
        else:
            assert False

        try:
            JalaliDateTime._check_time_fields("20", 1, 61, 1000)
        except TypeError:
            assert True
        else:
            assert False

    def test_others(self):
        self.assertTrue(JalaliDateTime.fromtimestamp(time.time()) <= JalaliDateTime.now())
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc).timestamp(), 578723400)
        self.assertEqual(JalaliDateTime.fromtimestamp(578723400, pytz.utc),
                         JalaliDateTime(1367, 2, 14, 4, 30, 0, 0, pytz.utc))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).jdate(), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).date(), date(1988, 5, 4))
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).replace(tzinfo=pytz.utc).__repr__(),
                         'JalaliDateTime(1367, 2, 14, 4, 30, tzinfo=<UTC>)')
        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 4, 4444).replace(year=1395, day=3, minute=59),
                         JalaliDateTime(1395, 2, 3, 4, 59, 4, 4444))

        self.assertEqual(JalaliDateTime.now(pytz.utc).tzname(), "UTC")
        self.assertIsNone(JalaliDateTime.today().tzname())
        self.assertIsNone(JalaliDateTime.today().dst())

        self.assertEqual(JalaliDateTime(1367, 2, 14, 4, 30, 0, 0).ctime(), "Chaharshanbeh 14 Ordibehesht 1367 04:30:00")
        self.assertEqual(JalaliDateTime(1396, 7, 27, 21, 48, 0, 0).ctime(), "Panjshanbeh 27 Mehr 1396 21:48:00")
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
        self.assertEqual(JalaliDateTime(1369, 7, 1, 14, 0, 10, 0, pytz.utc).strftime("%X %p %z %Z"), "14:00:10 PM +0000 UTC")
        self.assertEqual(JalaliDateTime(1369, 7, 1, 14, 0, 10, 0, pytz.utc).strftime("%c"), "Yekshanbeh 01 Mehr 1369 14:00:10")
        self.assertEqual(JalaliDateTime(1369, 7, 1, 11, 0, 10, 553, pytz.utc).strftime("%I:%M:%S.%f %p"), "11:00:10.000553 AM")
        self.assertEqual(JalaliDateTime(1369, 7, 1, 14, 0, 10, 553, pytz.utc).strftime("%I:%M:%S.%f %p"), "02:00:10.000553 PM")

