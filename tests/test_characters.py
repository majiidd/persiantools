# -*- coding: utf-8 -*-
from unittest import TestCase

from nose import tools

from persiantools import characters
from persiantools import digits


class TestDigits(TestCase):
    def test_ar_to_fa(self):
        self.assertEqual(characters.ar_to_fa("السلام عليكم"), "السلام علیکم")
        characters.ar_to_fa("راك")  # return: راک

    def test_long_ar_to_fa(self):
        orig = "السلام عليكم ٠١٢٣٤٥٦٧٨٩"
        converted = characters.ar_to_fa(orig)
        converted = digits.ar_to_fa(converted)

        self.assertEqual(converted, "السلام علیکم ۰۱۲۳۴۵۶۷۸۹")

    def test_special_ar_chars_to_fa(self):
        self.assertEqual(
            characters.ar_to_fa("ظ ط ذ د ز ر و ، . ش س ي ب ل ا ت ن م ك ض ص ث ق ف غ ع ه خ ح ؟"),
            "ظ ط ذ د ز ر و ، . ش س ی ب ل ا ت ن م ک ض ص ث ق ف غ ع ه خ ح ؟")

    @tools.raises(ValueError)
    def test_int_arg(self):
        characters.ar_to_fa(12345)
