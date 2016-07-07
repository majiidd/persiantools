# -*- coding: utf-8 -*-
from unittest import TestCase

from persiantools import utils


class TestUtils(TestCase):
    def test_replace(self):
        self.assertEqual(utils.replace("Persian Tools", {"Persian": "Parsi", " ": "_"}), "Parsi_Tools")
        self.assertEqual(utils.replace("آب بی فلسفه می‌خوردم", {"آب": "آآآب", " ": "_"}), "آآآب_بی_فلسفه_می‌خوردم")

    def test_int(self):
        self.assertEqual(utils.check_int_field(100010001), 100010001)

        try:
            utils.check_int_field(1111.9999)
        except TypeError:
            assert True
        else:
            assert False

        try:
            utils.check_int_field("1000")
        except TypeError:
            assert True
        else:
            assert False
