import unittest

import utils.utils as utils


class TestUtils(unittest.TestCase):
    def test_circular_permute_dict_values(self):
        dict_a = {"a": 1, "b": 2, "c": 3}
        expected_result = {"a": 2, "b": 3, "c": 1}
        self.assertEqual(utils.circular_permute_dict_values(dict_a), expected_result)
        self.assertEqual(utils.circular_permute_dict_values({}), {})
        self.assertEqual(utils.circular_permute_dict_values({"x": 10}), {"x": 10})

    def test_get_next_list_element(self):
        input_list = ["a", "b", "c", "d"]
        self.assertEqual(utils.get_next_list_element(input_list, "a"), "b")
        self.assertEqual(utils.get_next_list_element(input_list, "d"), "a")
        input_list = []
        with self.assertRaises(ValueError):
            utils.get_next_list_element(input_list, "a")

    def test_get_nonzero_indices_of_2d_list(self):
        input_list = [[0, 0, 0], [0, 1, 0], [1, 0, 0]]
        self.assertEqual(
            utils.get_nonzero_indices_of_2d_list(input_list), [(1, 1), (2, 0)]
        )
        input_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(utils.get_nonzero_indices_of_2d_list(input_list), [])

    def test_slice_to_range(self):
        # Test with positive start, stop, and step
        s = slice(1, 5, 2)
        r = utils.slice_to_range(s, 6)
        self.assertEqual(list(r), [1, 3])

        # Too short
        r = utils.slice_to_range(s, 3)
        self.assertEqual(list(r), [1])

        # Test with negative start and stop
        s = slice(-5, -1)
        r = utils.slice_to_range(s, 6)
        self.assertEqual(list(r), [1, 2, 3, 4])

        # Test with negative step
        s = slice(5, 1, -1)
        r = utils.slice_to_range(s, 6)
        self.assertEqual(list(r), [5, 4, 3, 2])

    def test_slice_to_list(self):
        s = slice(1, 5, 2)
        r = utils.slice_to_range(s, 6)
        self.assertEqual(utils.slice_to_list(s, 6), list(r))

    def test_is_non_negative(self):
        self.assertTrue(utils.is_non_negative(5))
        self.assertFalse(utils.is_non_negative(-5))
        self.assertTrue(utils.is_non_negative(0))

    def test_is_non_negative_int(self):
        self.assertTrue(utils.is_non_negative_int(5))
        self.assertFalse(utils.is_non_negative_int(-5))
        self.assertTrue(utils.is_non_negative_int(0))
        self.assertFalse(utils.is_non_negative_int(3.14))

    def test_is_iterable(self):
        self.assertTrue(utils.is_iterable([]))
        self.assertFalse(utils.is_iterable(1))

    def test_is_iterable_of_length(self):
        self.assertTrue(utils.is_iterable_of_length([1, 2, 3], list, 3))
        self.assertFalse(utils.is_iterable_of_length([1, 2, 3], list, 4))
        self.assertTrue(utils.is_iterable_of_length((1, 2, 3), tuple, 3))
        self.assertTrue(utils.is_iterable_of_length("abc", str, 3))
        self.assertFalse(utils.is_iterable_of_length(123, int, 3))
        self.assertTrue(utils.is_iterable_of_length([1, 2, 3], list, min_length=3))
        self.assertTrue(utils.is_iterable_of_length([1, 2, 3, 4], list, min_length=3))
        self.assertFalse(utils.is_iterable_of_length([1, 2], list, min_length=3))
        self.assertTrue(utils.is_iterable_of_length([1, 2, 3], list, max_length=3))
        self.assertTrue(utils.is_iterable_of_length([1, 2], list, max_length=3))
        self.assertFalse(utils.is_iterable_of_length([1, 2, 3, 4], list, max_length=3))
        self.assertTrue(utils.is_iterable_of_length([1, 2, 3], list, 3, 2, 4))
        self.assertFalse(utils.is_iterable_of_length([1, 2, 3, 4], list, 3, 2, 4))

    def test_is_2d_coordinate(self):
        # Test with a valid 2D coordinate
        self.assertTrue(utils.is_2d_coordinate((1, 2)))

        # Test with an invalid 2D coordinate
        self.assertFalse(utils.is_2d_coordinate((1, 2, 3)))

        # Test with a non-tuple
        self.assertFalse(utils.is_2d_coordinate([1, 2]))

        # Test with a non-integer coordinate
        self.assertFalse(utils.is_2d_coordinate((1.5, 2)))

        # Test with a negative coordinate
        self.assertFalse(utils.is_2d_coordinate((-1, 2)))

        # Test with a valid 2D coordinate and max coordinates
        self.assertTrue(utils.is_2d_coordinate((1, 2), (3, 4)))

        # Test with an invalid 2D coordinate and max coordinates
        self.assertFalse(utils.is_2d_coordinate((3, 4), (3, 4)))


if __name__ == "__main__":
    unittest.main()
