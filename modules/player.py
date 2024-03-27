import utils.check_utils as check_utils
from modules.board import Board


class Player:
    def __init__(self, player_id, color):
        check_utils.check_is_non_negative_int("id", player_id)
        check_utils.check_is_instance("color", color, str)
        self.id = player_id
        self.color = color

    def __str__(self):
        return f"Player {self.id} with color {self.color}"

    def __repr__(self):
        return str(self)

    def get_color(self):
        return self.color

    def get_id(self):
        return self.id

    def get_own_pieces(self, board):
        check_utils.check_is_instance("board", board, Board)
        return board.is_colors_pieces(self.color)

    def get_allowed_moves(self, board):
        check_utils.check_is_instance("board", board, Board)
        allowed_moves = board.get_allowed_moves(self.color)
        no_allowed_moves = True
        for row in range(board.board_shape[0]):
            for column in range(board.board_shape[1]):
                if len(allowed_moves[row][column]) != 0:
                    no_allowed_moves = False
                    break

        if no_allowed_moves:
            raise ValueError(f"Player {self.id} has no allowed moves.")

        return allowed_moves

        # coordinates_of_own_pieces = utils.get_nonzero_indices_of_2d_list(own_pieces)

        # chosen_piece_coordinates =
        # random.choice(utils.get_nonzero_indices_of_2d_list(own_pieces))
        # allowed_moves_for_chosen_piece =
        # allowed_moves[chosen_piece_coordinates[0]][chosen_piece_coordinates[1]]
        # chosen_move_coordinates = random.choice(allowed_moves_for_chosen_piece)
        #
        # return chosen_piece_coordinates, chosen_move_coordinates
