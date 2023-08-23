import unittest

import torch

from modules.state import State

initial_board = torch.tensor(
    [
        [-3, -5, -4, -2, -1, -4, -5, -3],  # black
        [-6, -6, -6, -6, -6, -6, -6, -6],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [3, 5, 4, 2, 1, 4, 5, 3],  # white
    ]
)


class TestState(unittest.TestCase):
    def test_update_positions(self):
        # Create an instance of the state class
        state = State()

        # Call the update_positions method
        state.update_positions((6, 3), (4, 3))
        state.update_positions((0, 1), (2, 2))
        state.update_positions((7, 2), (5, 4))
        state.update_positions((2, 2), (4, 3))

        # Check that the board was updated correctly
        correct_board = torch.tensor(
            [
                [-3, 0, -4, -2, -1, -4, -5, -3],  # black
                [-6, -6, -6, -6, -6, -6, -6, -6],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, -5, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0],
                [6, 6, 6, 0, 6, 6, 6, 6],
                [3, 5, 0, 2, 1, 4, 5, 3],  # white
            ]
        )

        self.assertTrue(torch.equal(state.board, correct_board))

    def test_update_score(self):
        state = State(score=torch.tensor([3, 4, 1]))
        state.update_score(torch.tensor([2, 3, 1]))

        self.assertTrue(torch.equal(state.score, torch.tensor([5, 7, 2])))

    def test_update_turn_number(self):
        state = State()
        state.next_turn()

        self.assertEqual(state.turn_number, 1)
        self.assertEqual(state.player_turn, -1)

        state.next_turn()

        self.assertEqual(state.turn_number, 2)
        self.assertEqual(state.player_turn, 1)

    def test_update_game_count(self):
        state = State()
        state.update_game_count()

        self.assertEqual(state.game_count, 1)

    def test_update_player_colors(self):
        state = State(player_colors=[1, -1])
        state.update_player_colors()

        self.assertEqual(state.player_colors, [-1, 1])

    def test_game_end(self):
        state = State(
            score=torch.tensor([3, 4, 1]),
            player_colors=[1, -1],
            game_count=0,
            board=torch.zeros((8, 8)),
            turn_number=5,
            player_turn=-1,
        )
        state.game_end(torch.tensor([2, 3, 1]))

        self.assertTrue(torch.equal(state.score, torch.tensor([5, 7, 2])))
        self.assertEqual(state.game_count, 1)
        self.assertEqual(state.player_colors, [-1, 1])
        self.assertTrue(torch.equal(state.board, initial_board))
        self.assertEqual(state.turn_number, 0)
        self.assertEqual(state.player_turn, 1)

    def test_reset(self):
        state = State(
            board=torch.zeros((8, 8)),
            turn_number=5,
            player_turn=-1,
        )

        state.reset()

        self.assertTrue(torch.equal(state.board, initial_board))
        self.assertEqual(state.turn_number, 0)
        self.assertEqual(state.player_turn, 1)

    def test_get_player_color(self):
        state = State(player_colors=[1, -1])
        player_color = state.get_player_color(0)

        self.assertEqual(player_color, 1)

        player_color = state.get_player_color(1)

        self.assertEqual(player_color, -1)

    def test_get_player_positions(self):
        state = State(board=torch.tensor([[1, 2], [-1, -2]]), player_colors=[1, -1])
        player_positions = state.get_player_positions(0)

        self.assertTrue(
            torch.equal(player_positions, torch.tensor([[True, True], [False, False]]))
        )

        player_positions = state.get_player_positions(1)

        self.assertTrue(
            torch.equal(player_positions, torch.tensor([[False, False], [True, True]]))
        )

    def test_get_player_pieces_and_coordinates(self):
        state = State(board=torch.tensor([[1, 2], [-1, -2]]), player_colors=[1, -1])
        pieces, coordinates = state.get_player_pieces_and_coordinates(0)

        self.assertTrue(torch.equal(pieces, torch.tensor([1, 2])))
        self.assertTrue(torch.equal(coordinates, torch.tensor([[0, 0], [0, 1]])))
