import unittest

from modules.board import Board
from modules.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(1, "white")

    def test_init(self):
        self.assertEqual(self.player.id, 1)
        self.assertEqual(self.player.color, "white")
        with self.assertRaises(ValueError):
            Player(-1, "white")
        with self.assertRaises(TypeError):
            Player(1, 1)

    def test_get_color(self):
        self.assertEqual(self.player.get_color(), self.player.color)

    def test_get_id(self):
        self.assertEqual(self.player.get_id(), self.player.id)

    def test_get_move(self):

        with self.assertRaises(ValueError):
            self.player.get_move(Board(player_colors=["red", "black"]))

        with self.assertRaises(ValueError):
            board = Board(player_colors=["white", "black"])
            board[0, 4] = None
            board[1, :] = None

            self.player.get_move(board)

        with self.assertRaises(TypeError):
            self.player.get_move("Not a board")


if __name__ == "__main__":
    unittest.main()
