import os
import sys
import unittest

import torch

current_dir = os.getcwd()
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)
from src.state import State


class TestState(unittest.TestCase):
    def test_update_positions(self):
        # Create an instance of the state class
        state = State()

        # Call the update_positions method
        state.update_positions((6, 3), (4, 3))
        state.update_positions((0, 1), (2, 2))
        state.update_positions((7, 2), (5, 4))
        state.update_positions((2, 2), (4, 3))

        # Check that the board was updated correctly
        correct_board = torch.tensor(
            [
                [-3, 0, -4, -2, -1, -4, -5, -3],  # black
                [-6, -6, -6, -6, -6, -6, -6, -6],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, -5, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0],
                [6, 6, 6, 0, 6, 6, 6, 6],
                [3, 5, 0, 2, 1, 4, 5, 3],  # white
            ]
        )

        self.assertTrue(torch.equal(state.board, correct_board))
