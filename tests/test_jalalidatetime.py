# -*- coding: utf-8 -*-
from datetime import datetime
from unittest import TestCase

from persiantools.jdatetime import JalaliDateTime


class TestJalaliDate(TestCase):
    def test_base(self):
        self.assertEqual(JalaliDateTime(1367, 2, 14, 14, 0, 0, 0),
                         JalaliDateTime.to_jalali(datetime(1988, 5, 4, 14, 0, 0, 0)))
