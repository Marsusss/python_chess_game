import unittest

from modules.ai_player import AIPlayer
from modules.board import Board


class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.ai_player = AIPlayer("1", "white")
        self.board = Board(player_colors=["white", "black"])

    def test_init(self):
        self.assertEqual(self.ai_player.id, "1")
        self.assertEqual(self.ai_player.color, "white")
        self.assertEqual(self.ai_player.model_name, "random")
        with self.assertRaises(TypeError):
            AIPlayer(1, "white")

        with self.assertRaises(TypeError):
            AIPlayer("1", 1)

        with self.assertRaises(ValueError):
            AIPlayer("1", "white", "not a known model name")

        with self.assertRaises(NotImplementedError):
            self.ai_player.get_probabilities(self.board)

        with self.assertRaises(TypeError):
            AIPlayer("1", "white", "random", {"seed": "not an int"})

    def test_str(self):
        self.assertEqual(
            str(self.ai_player),
            "Player_type: AIPlayer\nID: 1\nColor: white\nModel: random",
        )

    def test_get_move(self):
        chosen_piece, chosen_move = self.ai_player.get_move(self.board)
        self.assertTrue(
            len(
                self.ai_player.get_allowed_moves(self.board)[chosen_piece[0]][
                    chosen_piece[1]
                ]
            )
            > 0
        )

        self.assertIn(
            chosen_move,
            self.ai_player.get_allowed_moves(self.board)[chosen_piece[0]][
                chosen_piece[1]
            ],
        )

        self.ai_player1 = AIPlayer("1", "white", model_config={"seed": 0})
        chosen_piece1, chosen_move1 = self.ai_player1.get_move(self.board)
        self.ai_player2 = AIPlayer("1", "white", model_config={"seed": 0})
        chosen_piece2, chosen_move2 = self.ai_player2.get_move(self.board)

        self.assertEqual((chosen_piece1, chosen_move1), (chosen_piece2, chosen_move2))

        with self.assertRaises(TypeError):
            self.ai_player.get_move("Not a board")

        with self.assertRaises(ValueError):
            self.board[0, 4] = None
            self.board[1, :] = None

            self.ai_player.get_move(self.board)


if __name__ == "__main__":
    unittest.main()
