import utils.check_utils as check_utils
from modules.board import Board


class Game_log:
    def __init__(self, game_number=0, player_id_to_color=None):
        if player_id_to_color is None:
            player_id_to_color = {"p1": "white", "p2": "black"}

        check_utils.check_is_non_negative_int("game_number", game_number)
        check_utils.check_is_instance("player_id_to_color", player_id_to_color, dict)
        if "p1" not in player_id_to_color or "p2" not in player_id_to_color:
            raise ValueError("player_id_to_color must have keys 'p1' and 'p2'")
        if player_id_to_color["p1"] not in ["white", "black"] or player_id_to_color[
            "p2"
        ] not in [
            "white",
            "black",
        ]:
            raise ValueError("player colors must be 'white' or 'black'")

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
        check_utils.check_is_instance("board_0", new_board, Board)
        if len(self) > 0:
            if not self.boards[0].is_similar_to(new_board):
                raise ValueError(
                    f"Expected new board to be similar to other boards:\n "
                    f"player_colors = {self[0].player_colors},\n "
                    f"shape = {self[0].board_shape}\n"
                    f"but got:\n"
                    f"player_colors = {new_board.player_colors},\n "
                    f"shape = {new_board.board_shape}\n"
                )

        self.boards.append(new_board)

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
