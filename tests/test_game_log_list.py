import unittest

from modules.board import Board
from modules.game_log import Game_log
from modules.game_log_list import Game_log_list


class TestGameLogList(unittest.TestCase):
    def setUp(self):
        self.log_list = Game_log_list(["white", "black"])
        self.game_log = Game_log(1, {"p1": "white", "p2": "black"})
        self.board_0 = Board(player_colors=["white", "black"])
        self.boards = [self.board_0]
        for board in self.boards:
            self.game_log.update_log(board)

        self.game_logs = [self.game_log]
        for game_log in self.game_logs:
            self.log_list.update_list(game_log)

    def test_getitem(self):
        self.assertEqual(self.log_list[:], self.game_logs[:])

    def test_init(self):
        self.assertEqual(self.log_list.player_colors, ["white", "black"])
        self.assertEqual(self.log_list.log_list, [self.game_log])

        with self.assertRaises(ValueError):
            Game_log_list([])  # less than two players

    def test_len(self):
        self.assertEqual(len(self.log_list), len(self.log_list.log_list))

    def test_iter(self):
        for i, log in enumerate(self.log_list):
            self.assertEqual(log, self.game_logs[i])

        self.assertEqual(i, len(self.log_list) - 1)

    def test_str(self):
        self.assertEqual(str(self.log_list), self.log_list.list_as_string())

    def test_repr(self):
        self.assertEqual(repr(self.log_list), str(self.log_list))

    def test_update_list(self):
        new_game_log = Game_log(2, {"p1": "black", "p2": "white"})
        self.board_1 = Board(player_colors=list(new_game_log.player_id_to_color.keys()))
        new_game_log.update_log(self.board_1)
        self.log_list.update_list(new_game_log)
        self.assertEqual(len(self.log_list), 2)
        self.assertEqual(self.log_list[-1], new_game_log)

        with self.assertRaises(TypeError):
            self.log_list.update_list("not a game log")  # not a Game_log instance

    def test_list_as_string(self):
        expected_str = (
            f"players: {self.log_list.player_colors}\n"
            f"game number: 1, player colors by id {self.game_log.player_id_to_color}\n"
        )
        self.assertEqual(self.log_list.list_as_string(), expected_str)

    def test_get_log(self):
        self.assertEqual(self.log_list.get_log(0), self.log_list[0])

    def test_get_player_colors(self):
        self.assertEqual(self.log_list.get_player_colors(), ["white", "black"])

    def test_get_log_list(self):
        self.assertEqual(self.log_list.get_log_list(), self.game_logs)


if __name__ == "__main__":
    unittest.main()
