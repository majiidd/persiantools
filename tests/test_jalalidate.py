# -*- coding: utf-8 -*-
import os
import pickle
from datetime import date, timedelta
from time import time
from unittest import TestCase

from persiantools.jdatetime import JalaliDate


class TestJalaliDate(TestCase):
    def test_shamsi_to_gregorian(self):
        self.assertEqual(JalaliDate(1367, 2, 14).to_gregorian(), date(1988, 5, 4))
        self.assertEqual(JalaliDate(1369, 7, 1).to_gregorian(), date(1990, 9, 23))
        self.assertEqual(JalaliDate(1395, 3, 21).to_gregorian(), date(2016, 6, 10))
        self.assertEqual(JalaliDate(1395, 12, 9).to_gregorian(), date(2017, 2, 27))
        self.assertEqual(JalaliDate(1395, 12, 30).to_gregorian(), date(2017, 3, 20))
        self.assertEqual(JalaliDate(1396, 1, 1).to_gregorian(), date(2017, 3, 21))
        self.assertEqual(JalaliDate(1400, 6, 31).to_gregorian(), date(2021, 9, 22))

        self.assertEqual(JalaliDate.today().to_gregorian(), date.today())

    def test_gregorian_to_shamsi(self):
        self.assertEqual(JalaliDate(date(1988, 5, 4)), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate(date(2122, 1, 31)), JalaliDate(1500, 11, 11))
        self.assertEqual(JalaliDate(date(2017, 3, 20)), JalaliDate(1395, 12, 30))
        self.assertEqual(JalaliDate(date(2000, 1, 1)), JalaliDate(1378, 10, 11))

        self.assertEqual(JalaliDate(date.today()), JalaliDate.today())

        self.assertEqual(JalaliDate.to_jalali(1990, 9, 23), JalaliDate(1369, 7, 1))
        self.assertEqual(JalaliDate.to_jalali(1990, 9, 23), JalaliDate(1369, 7, 1))
        self.assertEqual(JalaliDate.to_jalali(2013, 9, 16), JalaliDate(1392, 6, 25))
        self.assertEqual(JalaliDate.to_jalali(2018, 3, 20), JalaliDate(1396, 12, 29))

    def test_chackdate(self):
        self.assertEqual(JalaliDate.chack_date(1367, 2, 14), True)
        self.assertEqual(JalaliDate.chack_date(1395, 12, 30), True)
        self.assertEqual(JalaliDate.chack_date(1394, 12, 30), False)
        self.assertEqual(JalaliDate.chack_date(13, 13, 30), False)
        self.assertEqual(JalaliDate.chack_date(0, 0, 0), False)
        self.assertEqual(JalaliDate.chack_date(9378, 0, 0), False)
        self.assertEqual(JalaliDate.chack_date("1300", "1", "1"), False)
        self.assertEqual(JalaliDate.chack_date(1396, 12, 30), False)
        self.assertEqual(JalaliDate.chack_date(1397, 7, 1), True)

    def test_additions(self):
        self.assertEqual(JalaliDate(JalaliDate(1395, 3, 21)), JalaliDate(1395, 3, 21))

        self.assertEqual(JalaliDate.days_before_month(1), 0)
        self.assertEqual(JalaliDate.days_before_month(12), 336)

        self.assertEqual(JalaliDate(1395, 1, 1).replace(1367), JalaliDate(1367, 1, 1))
        self.assertEqual(JalaliDate(1395, 1, 1).replace(month=2), JalaliDate(1395, 2, 1))
        self.assertEqual(JalaliDate(1395, 1, 1, "en").replace(1367, 2, 14, "fa"), JalaliDate(1367, 2, 14, "en"))

        self.assertEqual(JalaliDate.fromtimestamp(time()), JalaliDate.today())
        self.assertEqual(JalaliDate.fromtimestamp(578707200), JalaliDate(1367, 2, 14))

        try:
            JalaliDate(1400, 1, 1, "us")
        except ValueError:
            assert True
        else:
            assert False

    def test_leap(self):
        self.assertEqual(JalaliDate.is_leap(1358), True)
        self.assertEqual(JalaliDate.is_leap(1366), True)
        self.assertEqual(JalaliDate.is_leap(1367), False)
        self.assertEqual(JalaliDate.is_leap(1370), True)
        self.assertEqual(JalaliDate.is_leap(1387), True)
        self.assertEqual(JalaliDate.is_leap(1395), True)
        self.assertEqual(JalaliDate.is_leap(1396), False)
        self.assertEqual(JalaliDate.is_leap(1399), True)
        self.assertEqual(JalaliDate.is_leap(1400), False)
        self.assertEqual(JalaliDate.is_leap(1403), True)

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

        self.assertEqual(JalaliDate(1367, 2, 14).weekday(), 4)
        self.assertEqual(JalaliDate(1393, 1, 1).weekday(), 6)
        self.assertEqual(JalaliDate(1394, 1, 1).weekday(), 0)
        self.assertEqual(JalaliDate(1394, 1, 1).isoweekday(), 1)
        self.assertEqual(JalaliDate(1395, 1, 1).weekday(), 1)
        self.assertEqual(JalaliDate(1395, 3, 21).weekday(), 6)
        self.assertEqual(JalaliDate(1396, 1, 1).weekday(), 3)
        self.assertEqual(JalaliDate(1397, 1, 1).weekday(), 4)
        self.assertEqual(JalaliDate(1400, 1, 1).weekday(), 1)
        self.assertEqual(JalaliDate(1400, 1, 1).isoweekday(), 2)

    def test_operators(self):
        self.assertEqual(JalaliDate(1367, 2, 14) == JalaliDate(date(1988, 5, 4)), True)
        self.assertEqual(JalaliDate(1367, 2, 14) != JalaliDate(date(1988, 5, 4)), False)
        self.assertEqual(JalaliDate(1367, 2, 14) < JalaliDate(1369, 1, 1), True)
        self.assertEqual(JalaliDate(1395, 12, 30) > JalaliDate(1395, 12, 29), True)
        self.assertEqual(JalaliDate(1395, 12, 30) >= JalaliDate(1395, 12, 30), True)
        self.assertEqual(JalaliDate(1367, 2, 14) <= JalaliDate(1369, 1, 1), True)
        self.assertEqual(JalaliDate(1367, 2, 14) >= JalaliDate(1369, 1, 1), False)

        self.assertEqual(JalaliDate(1395, 3, 21) + timedelta(days=2), JalaliDate(1395, 3, 23))
        self.assertEqual(JalaliDate(1395, 3, 21) + timedelta(days=-38), JalaliDate(1395, 2, 14))
        self.assertEqual(JalaliDate(1395, 3, 21) - timedelta(days=38), JalaliDate(1395, 2, 14))
        self.assertEqual(JalaliDate(1395, 3, 21) - JalaliDate(1395, 2, 14), timedelta(days=38))
        self.assertEqual(JalaliDate(1395, 3, 21) - date(2016, 5, 3), timedelta(days=38))
        self.assertEqual(JalaliDate(1395, 12, 30) - JalaliDate(1395, 1, 1), timedelta(days=365))

    def test_pickle(self):
        file = open("save.p", "wb")
        pickle.dump(JalaliDate(1369, 7, 1), file)
        file.close()

        file2 = open("save.p", "rb")
        j = pickle.load(file2)
        file2.close()

        self.assertEqual(j, JalaliDate(1369, 7, 1))

        os.remove("save.p")

    def test_hash(self):
        j1 = JalaliDate.today()
        j2 = JalaliDate(1369, 7, 1)
        j3 = JalaliDate(date(1990, 9, 23))

        self.assertEqual({j1: "today", j2: "mini1", j3: "mini2"},
                         {JalaliDate.today(): "today", JalaliDate(1369, 7, 1): "mini2"})
