import torch


class Game_log:
    def __init__(self, game_number=0, player_colors=None):
        if player_colors is None:
            player_colors = {"p1": "white", "p2": "black"}
        if not isinstance(game_number, int):
            raise TypeError("game_number must be an integer")
        if game_number <= 0:
            raise ValueError("game_number must be greater than 0")
        if not isinstance(player_colors, dict):
            raise TypeError("player_colors must be a dictionary")
        if "p1" not in player_colors or "p2" not in player_colors:
            raise ValueError("player_colors must have keys 'p1' and 'p2'")
        if player_colors["p1"] not in ["white", "black"] or player_colors["p2"] not in [
            "white",
            "black",
        ]:
            raise ValueError("player colors must be 'white' or 'black'")

        self.game_number = game_number
        self.player_colors = player_colors
        self.boards = []

    def __getitem__(self, turn_number):
        return self.get_board(turn_number)

    def update_log(self, board):
        if not isinstance(board, torch.Tensor):
            raise TypeError("board must be a torch tensor")
        if board.shape != (8, 8):
            raise ValueError("board must be an 8x8 tensor")

        self.boards.append(board)

    def get_log(self):
        return {
            "game_number": self.game_number,
            "player_colors": self.player_colors,
            "boards": self.boards,
        }

    def get_board(self, turn_number):
        if not isinstance(turn_number, int):
            raise TypeError(f"turn_number must be an integer, got {type(turn_number)}")
        if turn_number < 0:
            raise ValueError(
                f"turn_number must be greater than or equal to 0, got {turn_number}"
            )
        if turn_number >= len(self.boards):
            raise ValueError(
                f"turn_number must be less than the number of turns"
                f"({len(self.boards)}), got {turn_number}"
            )

        return self.boards[turn_number]

    def get_game_number(self):
        return self.game_number

    def get_player_colors(self):
        return self.player_colors
