import copy
import unittest

from modules.board import Board
from modules.pawn import Pawn


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.board = Board(["black", "white"])
        self.pawn = self.board[1, 0]

    def test_init(self):
        self.assertEqual(self.pawn.position, (1, 0))
        self.assertEqual(self.pawn.piece_type, "pawn")
        self.assertEqual(self.pawn.color, "black")
        self.assertEqual(self.pawn.id, 8)
        self.assertEqual(self.pawn.state["is_en_passant_able"], False)
        self.assertEqual(self.pawn.forward_direction, (1, 0))

    def test_eq(self):
        other_pawn = Pawn((1, 0), "black", 8, "down")
        self.assertEqual(self.pawn, other_pawn)

        other_pawn.id = 9
        self.assertEqual(self.pawn, other_pawn)

        other_pawn.color = "white"
        self.assertNotEqual(self.pawn, other_pawn)

        other_pawn.forward_direction = (-1, 0)
        other_pawn.color = "black"
        self.assertNotEqual(self.pawn, other_pawn)

        other_pawn.en_passant_cache = {(1, 1): (2, 1)}
        other_pawn.forward_direction = (1, 0)
        self.assertNotEqual(self.pawn, other_pawn)

    def test_neq(self):
        other_pawn = Pawn((1, 0), "black", 8, "down")
        self.assertNotEqual(self.pawn == other_pawn, self.pawn != other_pawn)

        other_pawn.id = 9
        self.assertNotEqual(self.pawn == other_pawn, self.pawn != other_pawn)

        other_pawn.color = "white"
        self.assertNotEqual(self.pawn == other_pawn, self.pawn != other_pawn)

        other_pawn.forward_direction = (-1, 0)
        other_pawn.color = "black"
        self.assertNotEqual(self.pawn == other_pawn, self.pawn != other_pawn)

        other_pawn.en_passant_cache = {(1, 1): (2, 1)}
        other_pawn.forward_direction = (1, 0)
        self.assertNotEqual(self.pawn == other_pawn, self.pawn != other_pawn)

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.pawn)
        self.assertIsNot(deepcopy_piece, self.pawn)
        for attr, value in vars(self.pawn).items():
            self.assertEqual(value, getattr(deepcopy_piece, attr))

    def test_get_allowed_moves(self):
        # Testing get single and double move
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 0), (3, 0)])

        # Test has_moved
        self.pawn["state"]["has_moved"] = True
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 0)])

        # Test attacking and blocking
        self.pawn["state"]["has_moved"] = False
        self.board._board[2][0] = Pawn((2, 0), "white", 40, "up")
        self.board._board[2][1] = Pawn((2, 1), "white", 41, "up")
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 1)])

        # Test en passant, just use print(self.board) to see what is happening.
        self.board._board[2][1] = None
        self.board._board[1][1] = Pawn((1, 1), "white", 41, "up")
        self.board._board[1][1]["state"]["is_en_passant_able"] = True
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 1)])
        self.assertEqual(self.pawn.en_passant_cache, {(2, 1): (1, 1)})

    def test_move(self):
        self.pawn.move((2, 0), self.board)
        self.assertEqual(self.pawn.position, (2, 0))

        with self.assertRaises(ValueError):
            self.pawn.move((2, 1), self.board)

        self.board[1, 1].move((3, 1), self.board)
        self.assertFalse(self.board[1, 1].state["is_en_passant_able"])


if __name__ == "__main__":
    unittest.main()
