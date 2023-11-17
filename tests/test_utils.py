import unittest

from utils import circular_permute_dict_values, get_next_list_element


class TestUtils(unittest.TestCase):
    def test_circular_permute_dict_values(self):
        dict_a = {"a": 1, "b": 2, "c": 3}
        expected_result = {"a": 2, "b": 3, "c": 1}
        self.assertEqual(circular_permute_dict_values(dict_a), expected_result)

    def test_get_next_list_element(self):
        input_list = ["a", "b", "c", "d"]
        self.assertEqual(get_next_list_element(input_list, "a"), "b")
        self.assertEqual(get_next_list_element(input_list, "d"), "a")


if __name__ == "__main__":
    unittest.main()
