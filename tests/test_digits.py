# -*- coding: utf-8 -*-
import pytest
from unittest import TestCase

from persiantools import digits


class TestDigits(TestCase):
    def test_en_to_fa(self):
        self.assertEqual(digits.en_to_fa("0987654321"), "۰۹۸۷۶۵۴۳۲۱")

    def test_ar_to_fa(self):
        self.assertEqual(digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١"), "۰۹۸۷۶۵۴۳۲۱")

    def test_fa_to_fa(self):
        self.assertEqual(digits.en_to_fa("۰۹۸۷۶۵۴۳۲۱"), "۰۹۸۷۶۵۴۳۲۱")

    def test_ar_en_to_fa(self):
        orig = "0987٦٥٤٣۲۱"
        converted = digits.en_to_fa(orig)
        converted = digits.ar_to_fa(converted)

        self.assertEqual(converted, "۰۹۸۷۶۵۴۳۲۱")

    def test_fa_to_en(self):
        self.assertEqual(digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱"), "0987654321")

    def test_fa_to_ar(self):
        self.assertEqual(digits.fa_to_ar("۰۹۸۷۶۵۴۳۲۱"), "٠٩٨٧٦٥٤٣٢١")

    def test_int_arg(self):
        with pytest.raises(TypeError):
            digits.en_to_fa(12345)
