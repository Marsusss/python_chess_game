import unittest

import utils.check_utils as check_utils


class CheckUtilsTests(unittest.TestCase):
    def test_check_is_instance(self):
        self.assertIsNone(check_utils.check_is_instance("var", "string", str))

        with self.assertRaises(TypeError):
            check_utils.check_is_instance("var", "string", int)

    def test_check_is_non_negative(self):
        self.assertIsNone(check_utils.check_is_non_negative("number", 1.1))

        with self.assertRaises(ValueError):
            check_utils.check_is_non_negative("number", -5)

    def test_check_is_non_negative_int(self):
        self.assertIsNone(check_utils.check_is_non_negative_int("integer", 5))

        with self.assertRaises(TypeError):
            check_utils.check_is_non_negative_int("integer", "string")

        with self.assertRaises(ValueError):
            check_utils.check_is_non_negative_int("integer", -10)

    def test_check_is_index(self):
        self.assertIsNone(check_utils.check_is_index(2, 5))

        with self.assertRaises(IndexError):
            check_utils.check_is_index(7, 5)


if __name__ == "__main__":
    unittest.main()
