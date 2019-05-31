# -*- coding: utf-8 -*-
from unittest import TestCase
import pytest

from persiantools import utils


class TestUtils(TestCase):
    def test_replace(self):
        self.assertEqual(utils.replace("Persian Tools", {"Persian": "Parsi", " ": "_"}), "Parsi_Tools")
        self.assertEqual(utils.replace("آب بی فلسفه می‌خوردم", {"آب": "آآآب", " ": "_"}), "آآآب_بی_فلسفه_می‌خوردم")
        self.assertEqual(utils.replace(u"ای بس که نباشیم و جهان خواهد بود", {u"ای": u"اایی", u"خواهد": u"خخووااههدد"}), u"اایی بس که نباشیم و جهان خخووااههدد بود")

    def test_int(self):
        self.assertEqual(utils.check_int_field(100010001), 100010001)

        with pytest.raises(TypeError):
            utils.check_int_field(1111.9999)

        with pytest.raises(TypeError):
            utils.check_int_field("1000")
