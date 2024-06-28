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

    def test_basic_replacement(self):
        text = "Hello, world! Welcome to the world of programming."
        replacements = {"world": "universe", "programming": "Python"}
        expected = "Hello, universe! Welcome to the universe of Python."
        self.assertEqual(utils.replace(text, replacements), expected)

    def test_no_replacement(self):
        text = "Hello, world!"
        replacements = {"universe": "galaxy"}
        expected = "Hello, world!"
        self.assertEqual(utils.replace(text, replacements), expected)

    def test_empty_string(self):
        text = ""
        replacements = {"world": "universe"}
        expected = ""
        self.assertEqual(utils.replace(text, replacements), expected)

    def test_empty_replacements(self):
        text = "Hello, world!"
        replacements = {}
        expected = "Hello, world!"
        self.assertEqual(utils.replace(text, replacements), expected)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            utils.replace(123, {"world": "universe"})

    def test_special_characters(self):
        text = "Hello, $world! Welcome to the $world of programming."
        replacements = {"$world": "universe"}
        expected = "Hello, universe! Welcome to the universe of programming."
        self.assertEqual(utils.replace(text, replacements), expected)

    def test_persian_language(self):
        text = "سلام دنیا! به دنیای برنامه نویسی خوش آمدید."
        replacements = {"دنیا": "جهان", "برنامه نویسی": "پایتون"}
        expected = "سلام جهان! به جهانی پایتون خوش آمدید."
        self.assertEqual(utils.replace(text, replacements), expected)
