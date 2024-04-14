import unittest

from modules.board import Board
from modules.game import Game
from modules.game_log import GameLog
from modules.pawn import Pawn


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(
            max_turns=100
        )  # Disabling max turns can cause infinite loops in current tests

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

        with self.assertRaises(TypeError):
            Game(
                player_id_to_player_config={
                    "p1": [],
                    "p2": {"color": "black", "type": "ai", "model": "random"},
                }
            )

        with self.assertRaises(ValueError):
            Game(
                player_id_to_player_config={
                    "p1": {"color": "black", "type": "ai", "model": "random"},
                    "p2": {"color": "black", "type": "ai", "model": "random"},
                }
            )

        with self.assertRaises(TypeError):
            Game(
                player_id_to_player_config={
                    "p1": {"color": 1, "type": "ai", "model": "random"},
                    "p2": {"color": "white", "type": "ai", "model": "random"},
                }
            )

        with self.assertRaises(ValueError):
            Game(
                player_id_to_player_config={
                    "p1": {"color": "black", "type": 1, "model": "random"},
                    "p2": {"color": "white", "type": "ai", "model": "random"},
                }
            )

        with self.assertRaises(ValueError):
            Game(
                player_id_to_player_config={
                    "p1": {"color": "black", "type": "ai", "model": "random"},
                    "p2": {"color": "white", "type": "ai", "model": 1},
                }
            )

        with self.assertRaises(NotImplementedError):
            Game(
                player_id_to_player_config={
                    "p1": {"color": "black", "type": "human", "model": "random"},
                    "p2": {"color": "white", "type": "ai", "model": "random"},
                }
            )

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

    def test_get_player_move(self):
        player_id = "p1"
        piece_position, target_position = self.game.get_player_move(player_id)
        piece = self.game.board[piece_position]
        self.assertTrue(
            self.game.board.is_on_board_and_occupied_by(
                piece_position, [self.game.player_id_to_color[player_id]]
            )
        )
        self.assertIn(target_position, piece.get_allowed_moves(self.game.board))

        with self.assertRaises(KeyError):
            self.game.get_player_move("p3")

        with self.assertRaises(TypeError):
            self.game.get_player_move(1)

    def test_check_game_state(self):
        player_id = self.game.player_ids[self.game.player_idx_turn]
        self.assertEqual(
            self.game.check_game_state(player_id),
            {"state": "in_progress", "winner": None},
        )

        for column_idx in range(self.game.board.board_shape[1]):
            self.game.board[1, column_idx] = Pawn(
                (1, column_idx), "black", 40 + column_idx, "up"
            )
            self.game.board[1, column_idx]["state"]["has_moved"] = True
            self.game.board[2, column_idx] = Pawn(
                (2, column_idx), "black", 50 + column_idx, "up"
            )

        self.assertEqual(
            self.game.check_game_state(current_player_id="p2"),
            {"state": "checkmate", "winner": "p2"},
        )

        for column_idx in range(3, 6):
            self.game.board[1, column_idx] = None

        self.assertEqual(
            self.game.check_game_state(current_player_id="p2"),
            {"state": "remis", "winner": None},
        )

        self.game.board[1, :] = None
        self.game.turn_count = 100
        self.assertEqual(
            self.game.check_game_state(current_player_id="p2"),
            {"state": "turn_limit", "winner": None},
        )

        self.game.board.threefold_repetition = True
        self.assertEqual(
            self.game.check_game_state(current_player_id="p2"),
            {"state": "remis", "winner": None},
        )

        with self.assertRaises(TypeError):
            self.game.check_game_state(current_player_id=1)

        self.game.turn_count = 101
        self.game.board.threefold_repetition = False
        with self.assertRaises(ValueError):
            self.game.check_game_state(current_player_id="p1")

    def test_move_piece(self):
        player_id = "p1"
        piece_position, target_position = self.game.get_player_move(player_id)
        game_log = self.game.get_game_log()
        piece = self.game.board[piece_position]

        self.game.move_piece(player_id, piece_position, target_position)
        self.assertIsNone(self.game.board[piece_position])
        self.assertEqual(self.game.board[target_position], piece)
        self.assertEqual(game_log[-1], self.game.board.board_as_list)

        with self.assertRaises(ValueError):  # Player tries to move opponent's piece
            self.game.move_piece("p2", piece_position, target_position)

        with self.assertRaises(ValueError):  # Player tries to move empty square
            self.game.move_piece(player_id, piece_position, target_position)

        with self.assertRaises(ValueError):  # Player tries illegal move
            self.game.move_piece(player_id, piece_position, (0, 0))

        with self.assertRaises(TypeError):  # Player tries to move a row
            self.game.move_piece(player_id, 1, target_position)

    def test_take_turn(self):
        current_turn = self.game.turn_count
        current_player_idx_turn = self.game.player_idx_turn
        self.game.take_turn()

        self.assertEqual(self.game.turn_count, current_turn + 1)
        self.assertEqual(
            self.game.player_idx_turn,
            (current_player_idx_turn + 1) % self.game.player_count,
        )
        while self.game.state["state"] == "in_progress":
            self.game.take_turn()
            print(self.game)
            print(self.game.board.board_cache)

    def test_play_game(self):
        self.game.play_game()
        self.assertNotEqual(self.game.state["state"], "in_progress")


if __name__ == "__main__":
    unittest.main()
