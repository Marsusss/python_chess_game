import copy

from modules.chess_piece import ChessPiece


class Pawn(ChessPiece):
    def __init__(self, position, color, id, forward_direction):
        super().__init__(position, "pawn", color, id)
        self.state["has_moved"] = False
        self.state["just_double_moved"] = False
        forward_directions = {"up": (-1, 0), "down": (1, 0)}
        if forward_direction not in forward_directions.keys():
            raise ValueError(
                f"Expected forward_direction to be in "
                f"{forward_directions.keys()}, "
                f"got {forward_direction}"
            )

        self.state["forward_direction"] = forward_direction
        self.forward_direction = forward_directions[forward_direction]

    def __deepcopy__(self, memodict={}):
        deepcopy = super().__deepcopy__()
        deepcopy.state["has_moved"] = copy.deepcopy(self.state["has_moved"])
        deepcopy.state["just_double_moved"] = copy.deepcopy(
            self.state["just_double_moved"]
        )
        deepcopy.state["forward_direction"] = copy.deepcopy(
            self.state["forward_direction"]
        )
        return deepcopy

    def get_allowed_moves(self, board):
        allowed_moves = []

        new_position = (self.position[0] + self.forward_direction[0], self.position[1])
        if board.is_on_board(new_position):
            if not board.is_occupied(new_position):
                allowed_moves.append(new_position)
                new_position = (
                    self.position[0] + 2 * self.forward_direction[0],
                    self.position[1],
                )
                if not self["state"]["has_moved"] and not board.is_occupied(
                    new_position
                ):
                    allowed_moves.append(new_position)

        for dx in [-1, 1]:
            new_position = (
                self.position[0] + self.forward_direction[0],
                self.position[1] + dx,
            )
            if board.is_on_board(new_position):
                if board.is_occupied(new_position):
                    if board[new_position].color != self.color:
                        allowed_moves.append(new_position)

            neighbouring_position = (self.position[0], self.position[1] + dx)
            if board.is_on_board(neighbouring_position):
                if board.is_occupied(neighbouring_position):
                    if (
                        board[neighbouring_position].color != self.color
                        and board[neighbouring_position]["type"] == "pawn"
                    ):
                        if board[neighbouring_position]["state"]["just_double_moved"]:
                            allowed_moves.append(new_position)

        return allowed_moves

    def move(self, new_position, board):  # NOT TESTABLE
        super().move(new_position, board)
        self.state["has_moved"] = True
        self.state["just_double_moved"] = abs(new_position[0] - self.position[0]) == 2
