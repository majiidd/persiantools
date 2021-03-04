import pytest

from persiantools import numbers


class TestNumbers(TestCase):

    def test_simple_digit_to_letter(self):

        self.assertEqaul(
            numbers.number_to_leter(121274564538922),
            'صد و بیست و یک تریلیون و دویست و هفتاد و چهار میلیارد و پانصد و شصت و چهار میلیون و پانصد و سی و هشت هزار و نهصد و بیست و دو '
        )


    def test_farsi_digit_to_letter(self):

        self.assertEqual(
            numbers.number_to_leter('۱212۷4564۵389۲2'),
            'صد و بیست و یک تریلیون و دویست و هفتاد و چهار میلیارد و پانصد و شصت و چهار میلیون و پانصد و سی و هشت هزار و نهصد و بیست و دو '
        )

