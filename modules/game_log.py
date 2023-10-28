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

    def get_board(self, turn):
        if not isinstance(turn, int):
            raise TypeError("turn must be an integer")
        if turn < 0:
            raise ValueError("turn must be greater than or equal to 0")

        if turn < len(self.boards):
            return self.boards[turn]
        else:
            return None
