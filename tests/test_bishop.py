import copy
import unittest

from modules.bishop import Bishop
from modules.board import Board


class TestBishop(unittest.TestCase):
    def setUp(self):
        self.board = Board(["black", "white"])
        self.bishop = self.board[0, 2]

    def test_init(self):
        self.assertEqual(self.bishop.position, (0, 2))
        self.assertEqual(self.bishop.piece_type, "bishop")
        self.assertEqual(self.bishop.color, "black")
        self.assertEqual(self.bishop.id, 2)

    def test_eq(self):
        other_bishop = Bishop((0, 2), "black", 2)
        self.assertEqual(self.bishop, other_bishop)

        other_bishop.id = 5
        self.assertEqual(self.bishop, other_bishop)

        other_bishop.color = "white"
        self.assertNotEqual(self.bishop, other_bishop)

    def test_neq(self):
        other_bishop = Bishop((0, 2), "black", 2)
        self.assertNotEqual(self.bishop == other_bishop, self.bishop != other_bishop)

        other_bishop.id = 5
        self.assertNotEqual(self.bishop == other_bishop, self.bishop != other_bishop)

        other_bishop.color = "white"
        self.assertNotEqual(self.bishop == other_bishop, self.bishop != other_bishop)

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.bishop)
        self.assertIsNot(deepcopy_piece, self.bishop)
        for attr, value in vars(self.bishop).items():
            self.assertEqual(value, getattr(deepcopy_piece, attr))

    def test_get_allowed_moves(self):
        # Test can't move in initial state (blocked by pawns)
        self.assertEqual(self.bishop.get_allowed_moves(self.board), [])

        # Test move when pawns are cleared
        self.board[1, :] = None
        self.assertEqual(
            self.bishop.get_allowed_moves(self.board),
            [(1, 1), (2, 0), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)],
        )

        # Test capturing and blocked by own piece
        self.board[4, 6] = Bishop((4, 6), "white", 41)
        self.board[2, 0] = Bishop((2, 0), "black", 42)
        self.assertEqual(
            self.bishop.get_allowed_moves(self.board),
            [(1, 1), (1, 3), (2, 4), (3, 5), (4, 6)],
        )

    def test_move(self):
        self.board[1, :] = None
        self.bishop.move((2, 0), self.board)
        self.assertEqual(self.bishop.position, (2, 0))

        with self.assertRaises(ValueError):
            self.bishop.move((2, 1), self.board)


if __name__ == "__main__":
    unittest.main()
