import copy
import unittest

from modules.king import King


class TestKing(unittest.TestCase):
    def setUp(self):
        self.king = King((0, 0), "black", 1)

    def test_init(self):
        self.assertEqual(self.king.position, (0, 0))
        self.assertEqual(self.king.piece_type, "king")
        self.assertEqual(self.king.color, "black")
        self.assertEqual(self.king.id, 1)
        self.assertEqual(self.king.state["has_moved"], False)

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.king)
        self.assertIsNot(deepcopy_piece, self.king)
        self.assertEqual(deepcopy_piece.dict, self.king.dict)


if __name__ == "__main__":
    unittest.main()
