import copy

from modules.chess_piece import ChessPiece


class Pawn(ChessPiece):
    def __init__(self, position, color, id, forward_direction):
        super().__init__(position, "pawn", color, id)
        self.state["has_moved"] = False
        self.state["is_en_passant_able"] = False
        forward_directions = {"up": (-1, 0), "down": (1, 0)}
        if forward_direction not in forward_directions.keys():
            raise ValueError(
                f"Expected forward_direction to be in "
                f"{forward_directions.keys()}, "
                f"got {forward_direction}"
            )

        self.forward_direction = forward_directions[forward_direction]
        self.en_passant_cache = None

    def __deepcopy__(self, memodict={}):
        if self.forward_direction == (1, 0):
            forward_direction = "down"
        elif self.forward_direction == (-1, 0):
            forward_direction = "up"
        else:
            raise ValueError("forward direction is neither up nor down!")

        deepcopy = Pawn(
            copy.deepcopy(self.position),
            copy.deepcopy(self.color),
            copy.deepcopy(self.id),
            copy.deepcopy(forward_direction),
        )
        deepcopy.state["has_moved"] = copy.deepcopy(self.state["has_moved"])
        deepcopy.state["is_en_passant_able"] = copy.deepcopy(
            self.state["is_en_passant_able"]
        )
        deepcopy.forward_direction = copy.deepcopy(self.forward_direction)
        deepcopy.en_passant_cache = copy.deepcopy(self.en_passant_cache)

        return deepcopy

    def get_allowed_moves(self, board):
        super().get_allowed_moves(board)
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
                        if board[neighbouring_position]["state"]["is_en_passant_able"]:
                            allowed_moves.append(new_position)
                            self.en_passant_cache = {
                                new_position: neighbouring_position
                            }

        return allowed_moves

    def move(self, new_position, board):  # NOT TESTABLE
        super().move(new_position, board)
        if self.en_passant_cache is not None and new_position in self.en_passant_cache:
            board.en_passant_kill(self.en_passant_cache[new_position])

        self.state["has_moved"] = True
        just_double_moved = abs(new_position[0] - self.position[0]) == 2
        if just_double_moved:
            for dx in [-1, 1]:
                if board.is_on_board_and_occupied_by(
                    new_position, not_by_player_color=[self["color"]]
                ):
                    self.state["is_en_passant_able"] = True

        self.en_passant_cache = None
