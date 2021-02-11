from unittest import TestCase

from persiantools import utils


class TestUtils(TestCase):
    def test_replace(self):
        self.assertEqual(
            utils.replace("Persian Tools", {"Persian": "Parsi", " ": "_"}),
            "Parsi_Tools",
        )
        self.assertEqual(
            utils.replace("آب بی فلسفه می‌خوردم", {"آب": "آآآب", " ": "_"}),
            "آآآب_بی_فلسفه_می‌خوردم",
        )
        self.assertEqual(
            utils.replace(
                "ای بس که نباشیم و جهان خواهد بود",
                {"ای": "اایی", "خواهد": "خخووااههدد"},
            ),
            "اایی بس که نباشیم و جهان خخووااههدد بود",
        )
