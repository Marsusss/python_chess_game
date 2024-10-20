import copy

from modules.chess_piece import ChessPiece


class Knight(ChessPiece):
    def __init__(self, position, color, id):
        super().__init__(position, "knight", color, id)

    def __deepcopy__(self, memodict={}):
        deepcopy = Knight(
            copy.deepcopy(self.position),
            copy.deepcopy(self.color),
            copy.deepcopy(self.id),
        )
        return deepcopy

    def get_allowed_moves(self, board):
        super().get_allowed_moves(board)
        x, y = self.position
        allowed_moves = []

        for stride in [[1, 2], [2, 1]]:
            for dx in [-stride[0], stride[0]]:
                for dy in [-stride[1], stride[1]]:
                    new_position = (x + dx, y + dy)
                    if (
                        0 <= new_position[0] < board.board_shape[0]
                        and 0 <= new_position[1] < board.board_shape[1]
                    ):
                        if (
                            board[new_position] is None
                            or board[new_position]["color"] != self["color"]
                        ):
                            allowed_moves.append(new_position)

        return allowed_moves

    def move(self, new_position, board):
        super().move(new_position, board)
