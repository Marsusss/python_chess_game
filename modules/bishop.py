import copy

from modules.chess_piece import ChessPiece

class Bishop(ChessPiece):
    def __init__(self, position, color, id):
        super().__init__(position, "bishop", color, id)
        self.state["has_moved"] = False

    def __deepcopy__(self, memodict={}):
        deepcopy = Bishop(
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

        for dx in [-1, 1]:
            for dy in [-1, 1]:
                for dist in range(1,8):
                    new_position = (x + dx*dist, y + dy*dist)
                    if (
                        0 <= new_position[0] < board.board_shape[0]
                        and 0 <= new_position[1] < board.board_shape[1]
                    ):
                        if board[new_position] is None:
                            #Can go here and potentially further
                            allowed_moves.append(new_position)
                            
                        elif board[new_position]["color"] != self["color"]:
                            #Can go here but no further
                            allowed_moves.append(new_position)
                            break
                        
                        elif board[new_position]["color"] == self["color"]:
                            #Can't go here or any further
                            break
                    else:
                        #Save computation time if distance causes the new
                        #position to go beyond the board boundaries.
                        break

        return allowed_moves

    def move(self, new_position, board):
        super().move(new_position, board)
        self.state["has_moved"] = True
        board.king_positions[self.color] = new_position
