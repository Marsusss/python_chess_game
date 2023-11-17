import unittest

import torch

from modules.game_log import Game_log


class TestGameLog(unittest.TestCase):
    def setUp(self):
        self.log = Game_log(1, {"p1": "white", "p2": "black"})
        self.board = torch.zeros([8, 8])

    def test_init(self):
        self.assertEqual(self.log.game_number, 1)
        self.assertEqual(self.log.player_colors, {"p1": "white", "p2": "black"})
        self.assertEqual(self.log.boards, [])

    def test_update_log(self):
        self.log.update_log(self.board)
        self.assertEqual(len(self.log.boards), 1)
        self.assertTrue(torch.equal(self.log.boards[0], self.board))

    def test_get_log(self):
        self.log.update_log(self.board)
        log = self.log.get_log()
        expected_log = {
            "game_number": 1,
            "player_colors": {"p1": "white", "p2": "black"},
            "boards": [self.board],
        }
        self.assertEqual(log, expected_log)

    def test_get_board(self):
        self.log.update_log(self.board)
        board = self.log.get_board(0)
        self.assertTrue(torch.equal(board, self.board))

    def test_get_item(self):
        self.log.update_log(self.board)
        board = self.log[0]
        self.assertTrue(torch.equal(board, self.board))

    def test_get_game_number(self):
        self.assertEqual(self.log.get_game_number(), 1)

    def test_get_player_colors(self):
        self.assertEqual(self.log.get_player_colors(), {"p1": "white", "p2": "black"})

    def test_init_errors(self):
        with self.assertRaises(TypeError):
            Game_log("1", {"p1": "white", "p2": "black"})
        with self.assertRaises(ValueError):
            Game_log(0, {"p1": "white", "p2": "black"})
        with self.assertRaises(TypeError):
            Game_log(1, ["white", "black"])
        with self.assertRaises(ValueError):
            Game_log(1, {"p1": "white"})
        with self.assertRaises(ValueError):
            Game_log(1, {"p1": "green", "p2": "black"})

    def test_update_log_errors(self):
        with self.assertRaises(TypeError):
            self.log.update_log([0] * 64)
        with self.assertRaises(ValueError):
            self.log.update_log(torch.zeros([8, 7]))

    def test_get_board_errors(self):
        with self.assertRaises(TypeError):
            self.log.get_board("0")
        with self.assertRaises(ValueError):
            self.log.get_board(-1)


if __name__ == "__main__":
    unittest.main()
