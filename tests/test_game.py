import unittest

from modules.board import Board
from modules.game import Game
from modules.game_log import GameLog


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_init(self):
        self.assertIsInstance(self.game.board, Board)
        self.assertEqual(self.game.turn_count, 0)
        self.assertEqual(self.game.player_idx_turn, 0)
        self.assertEqual(self.game.state, {"state": "in_progress", "winner": None})
        with self.assertRaises(ValueError):
            Game(player_id_to_player_config={})
        with self.assertRaises(TypeError):
            Game(player_id_to_player_config="not a dictionary")
        with self.assertRaises(TypeError):
            Game(Board="Not a board")
        # with self.assertRaises(ValueError):
        #     Game(player_id_to_player_config = {
        #         "p1": {"color": "white", "type": "ai", "model": "random"},
        #         "p2": {"color": "green", "type": "ai", "model": "random"},
        #     })

    def test_str(self):
        self.assertIsInstance(str(self.game), str)

    def test_repr(self):
        self.assertIsInstance(repr(self.game), str)

    def test_getitem(self):
        self.assertEqual(self.game["state"], "in_progress")
        self.assertEqual(self.game["winner"], None)

    def test_get_board(self):
        self.assertIsInstance(self.game.get_board(), Board)

    def test_get_game_log(self):
        self.assertIsInstance(self.game.get_game_log(), GameLog)

    def test_get_player_id_to_player(self):
        self.assertIsInstance(self.game.get_player_id_to_player(), dict)

    def test_get_game_state(self):
        self.assertIsInstance(self.game.get_game_state(), dict)


if __name__ == "__main__":
    unittest.main()
