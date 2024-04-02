import random

import utils.utils as utils
from modules.player import Player


class AIPlayer(Player):
    def __init__(self, player_id, color, model_name="random"):
        super().__init__(player_id, color)
        self.model_name = model_name
        if model_name != "random":
            raise ValueError(f"Model {model_name} is not supported.")

    def __str__(self):
        return (
            f"Player_type: AIPlayer\nID: {self.id}\nColor: {self.color}\nModel: "
            f"{self.model_name}"
        )

    def get_move(self, board):
        allowed_moves = self.get_allowed_moves(board)
        own_pieces = self.get_own_pieces(board)
        coordinates_of_own_pieces = utils.get_nonzero_indices_of_2d_list(own_pieces)
        chosen_piece_coordinates = random.choice(coordinates_of_own_pieces)
        allowed_moves_for_chosen_piece = allowed_moves[chosen_piece_coordinates[0]][
            chosen_piece_coordinates[1]
        ]
        chosen_move_coordinates = random.choice(allowed_moves_for_chosen_piece)

        return chosen_piece_coordinates, chosen_move_coordinates

    def get_probabilities(self, board):
        raise NotImplementedError
