import copy
import unittest

from modules.board import Board
from modules.queen import Queen


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.board = Board(["black", "white"])
        self.queen = self.board[0, 3]

    def test_init(self):
        self.assertEqual(self.queen.position, (0, 3))
        self.assertEqual(self.queen.piece_type, "queen")
        self.assertEqual(self.queen.color, "black")
        self.assertEqual(self.queen.id, 3)

    def test_eq(self):
        other_queen = Queen((0, 3), "black", 3)
        self.assertEqual(self.queen, other_queen)

        other_queen.id = 5
        self.assertEqual(self.queen, other_queen)

        other_queen.color = "white"
        self.assertNotEqual(self.queen, other_queen)

    def test_neq(self):
        other_queen = Queen((0, 3), "black", 3)
        self.assertNotEqual(self.queen == other_queen, self.queen != other_queen)

        other_queen.id = 5
        self.assertNotEqual(self.queen == other_queen, self.queen != other_queen)

        other_queen.color = "white"
        self.assertNotEqual(self.queen == other_queen, self.queen != other_queen)

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.queen)
        self.assertIsNot(deepcopy_piece, self.queen)
        for attr, value in vars(self.queen).items():
            self.assertEqual(value, getattr(deepcopy_piece, attr))

    def test_get_allowed_moves(self):
        # Test can't move in initial state (blocked by pawns)
        self.assertEqual(self.queen.get_allowed_moves(self.board), [])

        # Test move when pawns are cleared
        self.board[1, :] = None
        self.board[0, 2] = None
        self.assertEqual(
            self.queen.get_allowed_moves(self.board),
            [
                (1, 2),
                (2, 1),
                (3, 0),
                (1, 4),
                (2, 5),
                (3, 6),
                (4, 7),
                (1, 3),
                (2, 3),
                (3, 3),
                (4, 3),
                (5, 3),
                (6, 3),
                (0, 2),
            ],
        )

        # Test capturing and blocked by own piece
        self.board[3, 6] = Queen((3, 6), "white", 41)
        self.board[2, 1] = Queen((2, 0), "black", 42)
        self.assertEqual(
            self.queen.get_allowed_moves(self.board),
            [
                (1, 2),
                (1, 4),
                (2, 5),
                (3, 6),
                (1, 3),
                (2, 3),
                (3, 3),
                (4, 3),
                (5, 3),
                (6, 3),
                (0, 2),
            ],
        )

    def test_move(self):
        self.board[1, :] = None
        self.queen.move((2, 1), self.board)
        self.assertEqual(self.queen.position, (2, 1))

        with self.assertRaises(ValueError):
            self.queen.move((2, 0), self.board)


if __name__ == "__main__":
    unittest.main()
