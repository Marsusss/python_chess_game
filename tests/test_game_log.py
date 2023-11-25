import unittest

import torch

from modules.game_log import Game_log


class TestGameLog(unittest.TestCase):
    def setUp(self):
        self.log = Game_log(1, {"p1": "white", "p2": "black"})
        self.board_0 = torch.zeros([8, 8])
        self.board_1 = torch.ones([8, 8])
        self.boards = [self.board_0]
        for board in self.boards:
            self.log.update_log(board)

    def test_init(self):
        self.assertEqual(self.log.game_number, 1)
        self.assertEqual(self.log.player_id_to_color, {"p1": "white", "p2": "black"})
        self.assertEqual(self.log.boards, [self.board_0])

    def test_len(self):
        self.assertEqual(len(self.log), len(self.log.boards))

    def test_iter(self):
        for i, log_entry in enumerate(self.log):
            self.assertTrue(torch.equal(log_entry, self.boards[i]))

        self.assertEqual(i, len(self.log) - 1)

    def test_update_log(self):
        current_log_length = len(self.log.boards)
        self.log.update_log(self.board_1)
        self.assertEqual(len(self.log.boards), current_log_length + 1)
        self.assertTrue(torch.equal(self.log[-1], self.board_1))

    def test_get_log(self):
        log = self.log.get_log()
        expected_log = {
            "game_number": self.log.game_number,
            "player_id_to_color": self.log.player_id_to_color,
            "boards": self.log.boards,
        }
        self.assertEqual(log, expected_log)

    def test_get_item(self):
        self.log.update_log(self.board_1)
        self.assertEqual(self.log[:], self.log.boards[:])

    def test_get_board(self):
        board = self.log.get_board(0)
        self.assertTrue(torch.equal(board, self.boards[0]))

    def test_get_game_number(self):
        self.assertEqual(self.log.get_game_number(), self.log.game_number)

    def test_get_player_colors(self):
        self.assertEqual(self.log.get_player_colors(), self.log.player_id_to_color)

    def test_init_errors(self):
        with self.assertRaises(TypeError):
            Game_log("1", {"p1": "white", "p2": "black"})
        with self.assertRaises(ValueError):
            Game_log(-1, {"p1": "white", "p2": "black"})
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
        with self.assertRaises(IndexError):
            self.log.get_board(len(self.log))


if __name__ == "__main__":
    unittest.main()
