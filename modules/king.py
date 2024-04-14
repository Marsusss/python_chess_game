import copy

from modules.chess_piece import ChessPiece


class King(ChessPiece):
    def __init__(self, position, color, id):
        super().__init__(position, "king", color, id)
        self.state["has_moved"] = False

    def __deepcopy__(self, memodict={}):
        deepcopy = King(
            copy.deepcopy(self.position),
            copy.deepcopy(self.color),
            copy.deepcopy(self.id),
        )
        deepcopy.state["has_moved"] = copy.deepcopy(self.state["has_moved"])
        return deepcopy

    def get_allowed_moves(self, board):  # NOT TESTABLE
        super().get_allowed_moves(board)
        x, y = self.position
        allowed_moves = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    new_position = (x + dx, y + dy)
                    if (
                        0 <= new_position[0] < board.board_shape[0]
                        and 0 <= new_position[1] < board.board_shape[1]
                    ):
                        if board[new_position] is None or (
                            board[new_position]["color"] != self["color"]
                        ):
                            allowed_moves.append(new_position)

        return allowed_moves

    def move(self, new_position, board):
        super().move(new_position, board)
        self.state["has_moved"] = True
        board.king_positions[self.color] = new_position
