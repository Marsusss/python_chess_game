import copy
import unittest

from modules.chess_piece import ChessPiece


class TestChessPiece(unittest.TestCase):
    def setUp(self):
        self.chess_piece = ChessPiece((0, 0), "king", "black", 1)

    def test_init(self):
        self.assertEqual(self.chess_piece.position, (0, 0))
        self.assertEqual(self.chess_piece.piece_type, "king")
        self.assertEqual(self.chess_piece.color, "black")
        self.assertEqual(self.chess_piece.id, 1)
        self.assertEqual(self.chess_piece.symbol, "\033[30m♚\033[0m")
        with self.assertRaises(TypeError):
            ChessPiece("not a tuple", "king", "black", 1)
        with self.assertRaises(ValueError):
            ChessPiece(("wrong", "length", "tuple"), "king", "black", 1)
        with self.assertRaises(TypeError):
            ChessPiece((0, "not an int"), "king", "black", 1)
        with self.assertRaises(ValueError):
            ChessPiece((0, -1), "king", "black", 1)
        with self.assertRaises(KeyError):
            ChessPiece((0, 0), "not in symbol schema", "black", 1)
        with self.assertRaises(KeyError):
            ChessPiece((0, 0), "king", "not in color codes", 1)
        with self.assertRaises(TypeError):
            ChessPiece((0, 0), "king", "black", "not an int")
        with self.assertRaises(ValueError):
            ChessPiece((0, 0), "king", "black", -1)

    def test_eq(self):
        other_chess_piece = ChessPiece((0, 0), "king", "black", 1)
        self.assertEqual(self.chess_piece, other_chess_piece)

        other_chess_piece.id = 2
        self.assertEqual(self.chess_piece, other_chess_piece)

        other_chess_piece.color = "white"
        self.assertNotEqual(self.chess_piece, other_chess_piece)

    def test_neq(self):
        other_chess_piece = ChessPiece((0, 0), "king", "black", 1)
        self.assertNotEqual(
            self.chess_piece == other_chess_piece, self.chess_piece != other_chess_piece
        )

        other_chess_piece.id = 2
        self.assertNotEqual(
            self.chess_piece == other_chess_piece, self.chess_piece != other_chess_piece
        )

        other_chess_piece.color = "white"
        self.assertNotEqual(
            self.chess_piece == other_chess_piece, self.chess_piece != other_chess_piece
        )

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.chess_piece)
        self.assertIsNot(deepcopy_piece, self.chess_piece)
        self.assertEqual(deepcopy_piece.dict, self.chess_piece.dict)

    def test_getitem(self):
        self.assertEqual(self.chess_piece["type"], "king")

    def test_str(self):
        self.assertEqual(str(self.chess_piece), self.chess_piece.symbol)

    def test_repr(self):
        self.assertEqual(repr(self.chess_piece), self.chess_piece.symbol)


if __name__ == "__main__":
    unittest.main()
