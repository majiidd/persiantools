from unittest import TestCase

import pytest

from persiantools import characters, digits


class TestDigits(TestCase):
    def test_ar_to_fa(self):
        self.assertEqual(characters.ar_to_fa("السلام عليكم"), "السلام علیکم")
        self.assertEqual(characters.ar_to_fa("HI ي"), "HI ی")
        self.assertEqual(characters.ar_to_fa("دِ بِ زِ ذِ شِ سِ ى ي ك"), "د ب ز ذ ش س ی ی ک")
        self.assertEqual(characters.ar_to_fa("دِ بِ زِ ذِ شِ سِ ى ي ك"), "د ب ز ذ ش س ی ی ک")
        self.assertEqual(
            characters.ar_to_fa("ظ ط ذ د ز ر و ، . ش س ي ب ل ا ت ن م ك ض ص ث ق ف غ ع ه خ ح ؟"),
            "ظ ط ذ د ز ر و ، . ش س ی ب ل ا ت ن م ک ض ص ث ق ف غ ع ه خ ح ؟",
        )

        self.assertEqual(characters.ar_to_fa(""), "")
        self.assertEqual(characters.ar_to_fa("123456"), "123456")
        self.assertEqual(characters.ar_to_fa("!@#$%^&*()"), "!@#$%^&*()")
        self.assertEqual(characters.ar_to_fa("123 ي"), "123 ی")

        with pytest.raises(TypeError):
            characters.ar_to_fa(12345)

        orig = "السلام عليكم ٠١٢٣٤٥٦٧٨٩"
        converted = characters.ar_to_fa(orig)
        converted = digits.ar_to_fa(converted)
        self.assertEqual(converted, "السلام علیکم ۰۱۲۳۴۵۶۷۸۹")

    def test_fa_to_fa(self):
        self.assertEqual(characters.ar_to_fa("السلام علیکم"), "السلام علیکم")
        self.assertEqual(characters.ar_to_fa("کیک"), "کیک")

    def test_fa_to_ar(self):
        self.assertEqual(characters.fa_to_ar("کیک"), "كيك")
        self.assertEqual(characters.fa_to_ar("سلام به همه"), "سلام به همه")

        text = "یکی بود یکی نبود"
        expected = "يكي بود يكي نبود"
        self.assertEqual(characters.fa_to_ar(text), expected)

        self.assertEqual(characters.fa_to_ar(""), "")
        self.assertEqual(characters.fa_to_ar("123456"), "123456")
        self.assertEqual(characters.fa_to_ar("!@#$%^&*()"), "!@#$%^&*()")
        self.assertEqual(characters.fa_to_ar("123 ک"), "123 ك")

        with pytest.raises(TypeError):
            characters.fa_to_ar(12345)
