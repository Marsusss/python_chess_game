import copy
import unittest

import torch

from modules.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(player_colors=["w", "b"])

    def test_init(self):
        self.assertEqual(self.board.player_colors, ["w", "b"])
        self.assertEqual(self.board._board.shape, (4, 8, 8))

    def test_getitem(self):
        self.assertTrue(torch.equal(self.board[:, 0], self.board._board[:, :, 0]))
        self.assertTrue(torch.equal(self.board["a1"], self.board._board[:, 0, 0]))
        self.assertTrue(torch.equal(self.board[0, 0], self.board._board[:, 0, 0]))

    def test_str(self):
        self.assertIsInstance(str(self.board), str)

    def test_repr(self):
        self.assertEqual(repr(self.board), str(self.board))

    def test_get_board(self):
        self.assertTrue(torch.equal(self.board.get_board(), self.board._board))

    def test_get_piece(self):
        self.assertTrue(
            torch.equal(self.board.get_piece((0, 0)), self.board._board[:, 0, 0])
        )

    def test_get_piece_by_string(self):
        self.assertTrue(
            torch.equal(
                self.board.get_piece_by_string("a1"), self.board._board[:, 0, 0]
            )
        )

    def test_move_piece(self):
        old_coordinate = (0, 0)
        new_coordinate = (1, 1)
        old_piece = self.board.get_piece(old_coordinate).clone()
        self.board.move_piece(old_coordinate, new_coordinate)
        self.assertTrue(torch.equal(self.board.get_piece(new_coordinate), old_piece))
        self.assertTrue(
            torch.equal(
                self.board.get_piece(old_coordinate),
                torch.tensor([0, 0, 0, 0], dtype=torch.uint8),
            )
        )

    def test_copy(self):
        copied_board = copy.copy(self.board)
        self.assertEqual(copied_board.player_colors, self.board.player_colors)
        self.assertTrue(torch.equal(copied_board._board, self.board._board))
        self.assertIsNot(copied_board, self.board)
        self.assertIs(copied_board._board, self.board._board)

    def test_deepcopy(self):
        deepcopy_board = copy.deepcopy(self.board)
        self.assertEqual(deepcopy_board.player_colors, self.board.player_colors)
        self.assertTrue(torch.equal(deepcopy_board._board, self.board._board))
        self.assertIsNot(deepcopy_board, self.board)
        self.assertIsNot(deepcopy_board._board, self.board._board)

    def test_init_invalid_player_colors(self):
        with self.assertRaises(TypeError):
            Board(player_colors={})
        with self.assertRaises(ValueError):
            Board(player_colors=["w"])  # not enough player colors

    def test_init_invalid_board_shape(self):
        with self.assertRaises(TypeError):
            Board(player_colors=["w", "b"], board=torch.rand(4, 2, 2))  # too small
        with self.assertRaises(TypeError):
            Board(player_colors=["w", "b"], board=torch.rand(4, 21, 21))  # too large

    def test_getitem_invalid_coordinate(self):
        with self.assertRaises(IndexError):
            self.board[8, 8]  # out of bounds
        with self.assertRaises(TypeError):
            self.board["invalid"]  # invalid string coordinate

    def test_string_to_coordinate_invalid_string(self):
        with self.assertRaises(TypeError):
            self.board.string_to_coordinate("invalid")  # too long
        with self.assertRaises(KeyError):
            self.board.string_to_coordinate("z1")  # invalid letter

    def test_move_piece_invalid_coordinate(self):
        with self.assertRaises(IndexError):
            self.board.move_piece((0, 0), (8, 8))  # out of bounds
        with self.assertRaises(ValueError):
            self.board.move_piece((2, 2), (0, 0))  # moving an empty space


if __name__ == "__main__":
    unittest.main()
