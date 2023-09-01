import unittest

import torch

from modules.rules import Rules


class TestState(unittest.TestCase):
    def test_coordinate_to_point(self):
        coordinates = [[4, 2], [5, 7], [6, 0]]
        rules = Rules()
        board_positions = rules.coordinates_to_points(coordinates)

        correct_board = torch.tensor(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertTrue(torch.equal(board_positions, correct_board))

    def test_is_blocked(self):
        rules = Rules()
        # Test case 1: is_own is True
        result = rules.is_blocked(True, False)
        self.assertEqual(result, (False, 0))

        # Test case 2: is_opponents is True
        result = rules.is_blocked(False, True)
        self.assertEqual(result, (False, 1))

        # Test case 3: both is_own and is_opponents are False
        result = rules.is_blocked(False, False)
        self.assertEqual(result, (True, 1))
