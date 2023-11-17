import unittest

from modules.score import Score


class TestScore(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def test_initial_values(self):
        self.assertEqual(self.score["p1"], 0)
        self.assertEqual(self.score["draw"], 0)
        self.assertEqual(self.score["p2"], 0)

    def test_set_score(self):
        self.score["p1"] = 5
        self.assertEqual(self.score["p1"], 5)

    def test_keys(self):
        keys = self.score.keys()
        self.assertEqual(set(keys), {"p1", "draw", "p2"})

    def test_values(self):
        values = self.score.values()
        self.assertEqual(set(values), {0})

    def test_update_score(self):
        self.score.update_score("p1")
        self.assertEqual(self.score["p1"], 1)

    def test_invalid_key(self):
        with self.assertRaises(KeyError):
            self.score["p3"] = 5

    def test_invalid_value_type(self):
        with self.assertRaises(TypeError):
            self.score["p1"] = "five"

    def test_negative_value(self):
        with self.assertRaises(ValueError):
            self.score["p1"] = -5

    def test_initial_values_with_custom_score(self):
        custom_score = {"fish": 1, "draw": 2, "cow": 3}
        score = Score(custom_score)
        self.assertEqual(score["fish"], 1)
        self.assertEqual(score["draw"], 2)
        self.assertEqual(score["cow"], 3)

    def test_invalid_score_type(self):
        with self.assertRaises(TypeError):
            Score("invalid")

    def test_invalid_score_keys(self):
        with self.assertRaises(ValueError):
            Score({"invalid": 0})

    def test_invalid_score_length(self):
        with self.assertRaises(ValueError):
            Score({"p1": 0, "draw": 0})

    def test_invalid_initial_value_type(self):
        with self.assertRaises(TypeError):
            Score({"p1": "one", "draw": 0, "p2": 0})

    def test_negative_initial_value(self):
        with self.assertRaises(ValueError):
            Score({"p1": -1, "draw": 0, "p2": 0})

    def test_update_score_invalid_key(self):
        with self.assertRaises(KeyError):
            self.score.update_score("p3")


if __name__ == "__main__":
    unittest.main()
