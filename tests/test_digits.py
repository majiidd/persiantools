# -*- coding: utf-8 -*-
from unittest import TestCase

from nose import tools

from persiantools import digits


class TestDigits(TestCase):
    def test_en_to_fa(self):
        self.assertEqual(digits.en_to_fa("0987654321"), "۰۹۸۷۶۵۴۳۲۱")

    def test_ar_to_fa(self):
        self.assertEqual(digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١"), "۰۹۸۷۶۵۴۳۲۱")

    def test_ar_en_to_fa(self):
        orig = "0987٦٥٤٣۲۱"
        converted = digits.en_to_fa(orig)
        converted = digits.ar_to_fa(converted)

        self.assertEqual(converted, "۰۹۸۷۶۵۴۳۲۱")

    @tools.raises(ValueError)
    def test_int_arg(self):
        digits.en_to_fa(12345)
