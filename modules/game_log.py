import utils.check_utils as check_utils
from modules.board import Board


class Game_log:
    def __init__(self, game_number=0, player_id_to_color=None):
        if player_id_to_color is None:
            player_id_to_color = {"p1": "white", "p2": "black"}

        check_utils.check_is_non_negative_int("game_number", game_number)
        check_utils.check_is_iterable_of_length(
            "player_id_to_color", player_id_to_color, dict, min_length=2
        )

        self.game_number = game_number
        self.player_id_to_color = player_id_to_color
        self.boards = []

    def __getitem__(self, turn_number):
        return self.boards[turn_number]

    def __len__(self):
        return len(self.boards)

    def __iter__(self):
        return iter(self.boards)

    def __str__(self):
        return (
            f"There are {len(self)} boards saved and the first element is:"
            f" {self.boards[0]}"
        )

    def __repr__(self):
        return str(self)

    def update_log(self, new_board):
        check_utils.check_is_instance("new_board", new_board, Board)
        self.check_board_is_similar(new_board)

        self.boards.append(new_board.board_as_list)

    def check_board_is_similar(self, board):
        if len(self) > 0:
            if (len(self.boards[0]), len(self.boards[0][0])) != board.board_shape:
                raise ValueError(
                    f"Expected new board to be similar to other boards:\n "
                    f"shape = {(len(self.boards[0]), len(self.boards[0][0]))}\n"
                    f"but got:\n"
                    f"shape = {board.board_shape}\n"
                )

            current_colors = self.player_id_to_color.values()
            for color in board.player_colors:
                if color not in current_colors:
                    raise ValueError(
                        f"Expected new board to be similar to other boards:\n "
                        f"player_colors = {self.player_id_to_color.values()},\n"
                        f"but got:\n"
                        f"player_colors = {board.player_colors}"
                    )

    def get_log(self):
        return {
            "game_number": self.game_number,
            "player_id_to_color": self.player_id_to_color,
            "boards": self.boards,
        }

    def get_board(self, turn_number):
        check_utils.check_is_index(turn_number, len(self.boards))

        return self.boards[turn_number]

    def get_game_number(self):
        return self.game_number

    def get_player_id_to_color(self):
        return self.player_id_to_color
