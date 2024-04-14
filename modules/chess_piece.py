import utils.check_utils as check_utils


class ChessPiece:
    symbol_schema = {
        "king": "♚",
        "queen": "♛",
        "rook": "♜",
        "bishop": "♝",
        "knight": "♞",
        "pawn": "♟",
    }
    color_codes = {
        "r": "\033[31m",
        "red": "\033[31m",
        "g": "\033[32m",
        "green": "\033[32m",
        "y": "\033[33m",
        "yellow": "\033[33m",
        "be": "\033[34m",
        "blue": "\033[34m",
        "m": "\033[35m",
        "magenta": "\033[35m",
        "c": "\033[36m",
        "cyan": "\033[36m",
        "w": "\033[37m",
        "white": "\033[37m",
        "b": "\033[30m",
        "black": "\033[30m",
        # Reset color
        "reset": "\033[0m",
    }

    def __init__(self, position, piece_type, color, id):
        check_utils.check_is_iterable_of_length("postion", position, tuple, 2)
        for coordinate in position:
            check_utils.check_is_non_negative_int("piece_coordinate", coordinate)

        check_utils.check_is_instance("piece_type", piece_type, str)
        if piece_type not in self.symbol_schema.keys():
            raise KeyError(
                f"piece_type must be in {self.symbol_schema.keys()}, got {piece_type}"
            )

        check_utils.check_is_instance("color", color, str)
        if color not in self.color_codes.keys():
            raise KeyError(f"color must be in {self.color_codes.keys()}, got {color}")

        check_utils.check_is_non_negative_int("piece_id", id)
        self.position = position
        self.piece_type = piece_type
        self.color = color
        self.id = id
        self.symbol = (
            f"{self.color_codes[self.color]}"
            f"{self.symbol_schema[self.piece_type]}"
            f'{self.color_codes["reset"]}'
        )
        self.state = {}
        self.dict = {
            "position": self.position,
            "type": self.piece_type,
            "color": self.color,
            "state": self.state,
            "symbol": self.symbol,
            "id": self.id,
        }

    def __hash__(self):
        return hash((self.position, self.piece_type, self.color, str(self.state)))

    def __eq__(self, other):
        if type(self) is type(other):
            return (
                self.position == other.position
                and self.piece_type == other.piece_type
                and self.color == other.color
                and self.state == other.state
            )

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, item):
        return self.dict[item]

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self)

    def get_allowed_moves(self, board):  # NOT TESTABLE
        from modules.board import Board

        check_utils.check_is_instance("board", board, Board)

        if board[self.position] != self:
            raise ValueError(
                f"Expected board[position] to be this piece ({repr(self)}), "
                f"but got {board[self.position]}"
            )

        check_utils.check_is_iterable_of_length(
            "board_shape", board.board_shape, tuple, 2
        )
        for dimension in board.board_shape:
            check_utils.check_is_non_negative_int("board_dimension", dimension)

    def move(self, new_position, board):  # NOT TESTABLE
        allowed_moves = self.get_allowed_moves(board)
        if new_position not in allowed_moves:
            raise ValueError(
                f"new_position {new_position} must be in allowed moves {allowed_moves}"
            )

        self.position = new_position
