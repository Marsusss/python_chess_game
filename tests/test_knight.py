import copy
import unittest

from modules.board import Board
from modules.knight import Knight


class TestChessPiece(unittest.TestCase):
    def setUp(self):
        self.knight = Knight((0, 0), "white", 1)
        self.board = Board(["white", "black"])

    def test_init(self):
        self.assertEqual(self.knight.position, (0, 0))
        self.assertEqual(self.knight.piece_type, "knight")
        self.assertEqual(self.knight.color, "white")
        self.assertEqual(self.knight.id, 1)

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.knight)
        self.assertIsNot(deepcopy_piece, self.knight)
        self.assertEqual(deepcopy_piece.dict, self.knight.dict)

    def test_get_allowed_moves(self):
        self.board[0, 0] = self.knight
        self.assertEqual(self.knight.get_allowed_moves(self.board), [(2, 1)])

        self.knight.position = (7, 5)
        self.board[7, 5] = self.knight
        self.assertEqual(
            self.knight.get_allowed_moves(self.board), [(6, 3), (6, 7), (5, 4), (5, 6)]
        )

    def test_move(self):
        self.board[0, 0] = self.knight
        with self.assertRaises(ValueError):
            self.knight.move((1, 2), self.board)

        self.knight.move((2, 1), self.board)
        self.assertEqual(self.knight.position, (2, 1))
        self.assertRaises(ValueError, self.knight.move, (2, 1), self.board)


if __name__ == "__main__":
    unittest.main()
