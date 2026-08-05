from unittest import TestCase

import pytest

from persiantools import digits


class TestDigits(TestCase):
    def test_en_to_fa(self):
        self.assertEqual(digits.en_to_fa("0987654321"), "۰۹۸۷۶۵۴۳۲۱")
        self.assertEqual(digits.en_to_fa("0987654321"), "۰۹۸۷۶۵۴۳۲۱")
        self.assertEqual(digits.en_to_fa("۰۹۸۷۶۵۴۳۲۱"), "۰۹۸۷۶۵۴۳۲۱")
        self.assertEqual(digits.en_to_fa("+0987654321 abcd"), "+۰۹۸۷۶۵۴۳۲۱ abcd")
        self.assertEqual(digits.en_to_fa(""), "")
        self.assertEqual(digits.en_to_fa("abcd"), "abcd")

        with pytest.raises(TypeError):
            digits.en_to_fa(12345)

    def test_ar_to_fa(self):
        self.assertEqual(digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١"), "۰۹۸۷۶۵۴۳۲۱")
        self.assertEqual(digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١"), "۰۹۸۷۶۵۴۳۲۱")
        self.assertEqual(digits.ar_to_fa(""), "")
        self.assertEqual(digits.ar_to_fa("abcd"), "abcd")

        orig = "0987٦٥٤٣۲۱"
        converted = digits.en_to_fa(orig)
        converted = digits.ar_to_fa(converted)

        self.assertEqual(converted, "۰۹۸۷۶۵۴۳۲۱")

        with pytest.raises(TypeError):
            digits.ar_to_fa(12345)

    def test_fa_to_en(self):
        self.assertEqual(digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱"), "0987654321")
        self.assertEqual(digits.fa_to_en(""), "")
        self.assertEqual(digits.fa_to_en("abcd"), "abcd")

        with pytest.raises(TypeError):
            digits.fa_to_en(12345)

    def test_fa_to_ar(self):
        self.assertEqual(digits.fa_to_ar("۰۹۸۷۶۵۴۳۲۱"), "٠٩٨٧٦٥٤٣٢١")
        self.assertEqual(digits.fa_to_ar(" ۰۹۸۷۶۵۴۳۲۱"), " ٠٩٨٧٦٥٤٣٢١")
        self.assertEqual(digits.fa_to_ar(""), "")
        self.assertEqual(digits.fa_to_ar("abcd"), "abcd")

        with pytest.raises(TypeError):
            digits.fa_to_ar(12345)

    def test_translate_type_errors(self):
        for func in (digits.en_to_fa, digits.ar_to_fa, digits.fa_to_en, digits.fa_to_ar):
            with pytest.raises(TypeError):
                func(None)
            with pytest.raises(TypeError):
                func(b"123")
            with pytest.raises(TypeError):
                func(["۱۲۳"])

    def test_translate_round_trip(self):
        english = "0123456789"
        self.assertEqual(digits.fa_to_en(digits.en_to_fa(english)), english)

        arabic = "٠١٢٣٤٥٦٧٨٩"
        self.assertEqual(digits.fa_to_ar(digits.ar_to_fa(arabic)), arabic)

    def test_to_letter(self):
        self.assertEqual(digits.to_word(0), "صفر")
        self.assertEqual(digits.to_word(1), "یک")
        self.assertEqual(digits.to_word(12), "دوازده")
        self.assertEqual(digits.to_word(49), "چهل و نه")
        self.assertEqual(digits.to_word(77), "هفتاد و هفت")
        self.assertEqual(digits.to_word(123), "یکصد و بیست و سه")
        self.assertEqual(digits.to_word(250), "دویست و پنجاه")
        self.assertEqual(digits.to_word(809), "هشتصد و نه")
        self.assertEqual(digits.to_word(1001), "یک هزار و یک")
        self.assertEqual(digits.to_word(3512), "سه هزار و پانصد و دوازده")
        self.assertEqual(digits.to_word(10000), "ده هزار")
        self.assertEqual(digits.to_word(20010), "بیست هزار و ده")
        self.assertEqual(digits.to_word(10001), "ده هزار و یک")
        self.assertEqual(digits.to_word(500253), "پانصد هزار و دویست و پنجاه و سه")
        self.assertEqual(digits.to_word(6000123), "شش میلیون و یکصد و بیست و سه")
        self.assertEqual(digits.to_word(1000000985), "یک میلیارد و نهصد و هشتاد و پنج")
        self.assertEqual(digits.to_word(100_000_000_000_004), "یکصد تریلیون و چهار")
        self.assertEqual(digits.to_word(9_512_026_000_000), "نه تریلیون و پانصد و دوازده میلیارد و بیست و شش میلیون")

        self.assertEqual(digits.to_word(-305), "منفی سیصد و پنج")
        self.assertEqual(digits.to_word(10.02), "ده و دو صدم")
        self.assertEqual(digits.to_word(15.007), "پانزده و هفت هزارم")
        self.assertEqual(digits.to_word(12519.85), "دوازده هزار و پانصد و نوزده و هشتاد و پنج صدم")
        self.assertEqual(digits.to_word(123.50), "یکصد و بیست و سه و پنج دهم")
        self.assertEqual(digits.to_word(123.456), "یکصد و بیست و سه و چهارصد و پنجاه و شش هزارم")
        self.assertEqual(digits.to_word(123.0), "یکصد و بیست و سه")
        self.assertEqual(digits.to_word(-123.0), "منفی یکصد و بیست و سه")

        self.assertEqual(
            digits.to_word(-0.1554845), "منفی یک میلیون و پانصد و پنجاه و چهار هزار و هشتصد و چهل و پنج ده میلیونیم"
        )

        with pytest.raises(digits.OutOfRangeException):
            digits.to_word(1000000000000001)

        with pytest.raises(digits.OutOfRangeException):
            digits.to_word(0.123456789012345)

        with pytest.raises(TypeError):
            digits.to_word("123")

    def test_fractional_part_too_long(self):
        old_mantissa = digits.MANTISSA
        try:
            digits.MANTISSA = ("دهم",)
            with self.assertRaises(ValueError, msg="Fractional part is too long"):
                # 0.15 -> left = "0", right = "15", right.rstrip("0") == "15"
                # mantissa_index = len("15") - 1 == 1, which is >= len(MANTISSA) == 1.
                digits.to_word(0.15)
        finally:
            digits.MANTISSA = old_mantissa


@pytest.mark.parametrize(
    "number,expected",
    [
        (1, "یک"),
        (2, "دو"),
        (3, "سه"),
        (4, "چهار"),
        (5, "پنج"),
        (6, "شش"),
        (7, "هفت"),
        (8, "هشت"),
        (9, "نه"),
        (10, "ده"),
        (11, "یازده"),
        (12, "دوازده"),
        (13, "سیزده"),
        (14, "چهارده"),
        (15, "پانزده"),
        (16, "شانزده"),
        (17, "هفده"),
        (18, "هجده"),
        (19, "نوزده"),
        (20, "بیست"),
        (30, "سی"),
        (40, "چهل"),
        (50, "پنجاه"),
        (60, "شصت"),
        (70, "هفتاد"),
        (80, "هشتاد"),
        (90, "نود"),
        (100, "یکصد"),
        (200, "دویست"),
        (300, "سیصد"),
        (400, "چهارصد"),
        (500, "پانصد"),
        (600, "ششصد"),
        (700, "هفتصد"),
        (800, "هشتصد"),
        (900, "نهصد"),
    ],
)
def test_to_word_word_tables(number, expected):
    assert digits.to_word(number) == expected


@pytest.mark.parametrize(
    "number,expected",
    [
        # exact boundaries between ranges
        (110, "یکصد و ده"),
        (1000, "یک هزار"),
        (1_000_000, "یک میلیون"),
        (1_000_000_000, "یک میلیارد"),
        (1_000_000_000_000, "یک تریلیون"),
        # zero chunks in the middle and at the end must be skipped
        (1_000_001, "یک میلیون و یک"),
        (1_000_000_001, "یک میلیارد و یک"),
        (1_000_000_000_001, "یک تریلیون و یک"),
        (2_000_000_000_000, "دو تریلیون"),
        # largest supported integer
        (
            999_999_999_999_999,
            "نهصد و نود و نه تریلیون و نهصد و نود و نه میلیارد"
            " و نهصد و نود و نه میلیون و نهصد و نود و نه هزار و نهصد و نود و نه",
        ),
        (
            -999_999_999_999_999,
            "منفی نهصد و نود و نه تریلیون و نهصد و نود و نه میلیارد"
            " و نهصد و نود و نه میلیون و نهصد و نود و نه هزار و نهصد و نود و نه",
        ),
    ],
)
def test_to_word_boundaries(number, expected):
    assert digits.to_word(number) == expected


@pytest.mark.parametrize("number", [10**15, 10**15 + 1, -(10**15), -(10**15) - 1])
def test_to_word_out_of_range(number):
    with pytest.raises(digits.OutOfRangeException):
        digits.to_word(number)


@pytest.mark.parametrize(
    "number,expected",
    [
        (0.0, "صفر"),
        (-0.0, "صفر"),
        # zero integer part: no "صفر و" prefix
        (0.5, "پنج دهم"),
        (-0.5, "منفی پنج دهم"),
        # 14 decimal places: the maximum supported precision
        (
            0.12345678901234,
            "دوازده تریلیون و سیصد و چهل و پنج میلیارد و ششصد و هفتاد و هشت میلیون"
            " و نهصد و یک هزار و دویست و سی و چهار صد تریلیونیم",
        ),
    ],
)
def test_to_word_float_edges(number, expected):
    assert digits.to_word(number) == expected


def test_to_word_float_integer_part_out_of_range():
    with pytest.raises(digits.OutOfRangeException):
        digits.to_word(1e15)


def test_to_word_scientific_notation_unsupported():
    # Current behavior: floats whose repr() uses scientific notation (e.g. 1e16,
    # 1e-7) are not supported and fail with a raw ValueError from str.split(".").
    with pytest.raises(ValueError):
        digits.to_word(1e16)
    with pytest.raises(ValueError):
        digits.to_word(1e-7)


@pytest.mark.parametrize("invalid", [None, "123", b"123", [123], (123,), {123}, 3 + 4j])
def test_to_word_type_errors(invalid):
    with pytest.raises(TypeError):
        digits.to_word(invalid)
