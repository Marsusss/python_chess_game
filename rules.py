import torch


class rules:
    def __init__(self):

    def is_move_valid(self, state, move):
        if move in self.get_allowed_moves(state):
            return True
        else:
            return False

    def get_allowed_moves(self, state, player):
        pieces, positions = state.get_player_pieces(player)
        move_list = []
        for i, piece in enumerate(pieces):
            self.get_allowed_move(self, state, piece, player, positions[i])
            # move_pattern = get_move_pattern(piece)
            # conv(self.board, move_pattern)

    def get_allowed_move(self, state, piece, player, position):
        coordinate = self.coordinate_to_point(position)
        if abs(piece) == 1:
            self.get_allowed_king_moves(self, state, player, position)
        if abs(piece) == 2:
            self.get_allowed_queen_moves(self, state, player, position)
        if abs(piece) == 3:
            self.get_allowed_rook_moves()
        if abs(piece) == 4:
            self.get_allowed_bishop_moves()
        if abs(piece) == 5:
            self.get_allowed_knight_moves()
        if abs(piece) == 6:
            self.get_allowed_pawn_moves(player)

    def coordinate_to_point(position):
        board_position = torch.zeros((8, 8))
        board_position[position] = 1
        return board_position

    def check_if_is_check(self, state, allowed_moves_coordinates, player, piece):
        for i, coordinate in enumerate(allowed_moves_coordinates):
            suggested_board = state.board
            suggested_board[coordinate] = piece
            suggested_board[from] = 0  # is empty
            check = self.is_check(self, suggested_board)
            if check:
                allowed_moves[coordinate] = 0
        return allowed_moves

    def is_check(self):
        # mock
        return False

    def is_mate(self):
        if self.is_check():
            # mock
            return False
        # mock
        return False

    def is_blocked(is_own, is_opponents):
        if is_own:
            return False, 0  # Is blocked, can not use field
        elif is_opponents:
            return False, 1  # Is blocked, can use field
        else:
            return True, 1  # Is not blocked, can use field

    def get_allowed_king_moves(self, state, player, position):
        own_board = state.get_player_positions(self, player)
        base = torch.tensor([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]])

        allowed_moves = torch.conv(base, self.coordinate_to_point(position))
        available_spaces = abs(own_board - 1)
        allowed_moves *= available_spaces
        allowed_moves_coordinates = torch.nonzero(allowed_moves)
        allowed_moves = check_if_is_check(
            self, state, allowed_moves_coordinates, player, 1)

        return allowed_moves

    def get_allowed_queen_moves(self, state, player, position, is_rook=False, is_bishop=False):
        own_positions = torch.nonzero(state.get_player_positions(self, player))
        opponent_positions = torch.nonzero(
            state.get_player_positions(self, player))
        dist_xy = position, 7-position
        allowed_moves = torch.zeros((8, 8))
        toggle_xp = True
        toggle_xm = True
        toggle_yp = True
        toggle_ym = True
        toggle_xpyp = True
        toggle_xpym = True
        toggle_xmyp = True
        toggle_xmym = True

        if is_rook:
            toggle_xpyp = False
            toggle_xpym = False
            toggle_xmyp = False
            toggle_xmym = False

        if is_bishop:
            toggle_xp = False
            toggle_xm = False
            toggle_yp = False
            toggle_ym = False

        for xy in range(1, max(dist_xy)):
            xp = position[0] + xy
            xm = position[0] - xy
            yp = position[1] + xy
            ym = position[1] - xy
            pos_xp = (xp, position[1])
            pos_xm = (xm, position[1])
            pos_yp = (position[0], xp)
            pos_ym = (position[0], xm)
            pos_xpyp = (xp, yp)
            pos_xpym = (xp, ym)
            pos_xmyp = (xm, yp)
            pos_xmym = (xm, ym)

            if toggle_xp:
                if xp <= 7:
                    toggle_xp, allowed_moves[pos_xp] = self.is_blocked(
                        own_positions[pos_xp], opponent_positions[pos_xp])
                else:
                    toggle_xp = False

            if toggle_xm:
                if xm >= 0:
                    toggle_xm, allowed_moves[pos_xm] = self.is_blocked(
                        own_positions[pos_xm], opponent_positions[pos_xm])
                else:
                    toggle_xm = False

            if toggle_yp:
                if yp <= 7:
                    toggle_yp, allowed_moves[pos_yp] = self.is_blocked(
                        own_positions[pos_yp], opponent_positions[pos_yp])
                else:
                    toggle_yp = False

            if toggle_ym:
                if ym >= 0:
                    toggle_ym, allowed_moves[pos_ym] = self.is_blocked(
                        own_positions[pos_ym], opponent_positions[pos_ym])
                else:
                    toggle_ym = False

            if toggle_xpyp:
                if xp <= 7 and yp <= 7:
                    toggle_xpyp, allowed_moves[pos_xpyp] = self.is_blocked(
                        own_positions[pos_xpyp], opponent_positions[pos_xpyp])
                else:
                    toggle_xpyp = False

            if toggle_xpym:
                if xp <= 7 and ym >= 0:
                    toggle_xpym, allowed_moves[pos_xpym] = self.is_blocked(
                        own_positions[pos_xpym], opponent_positions[pos_xpym])
                else:
                    toggle_xpym = False

            if toggle_xmyp:
                if xm >= 0 and yp <= 7:
                    toggle_xmyp, allowed_moves[pos_xmyp] = self.is_blocked(
                        own_positions[pos_xmyp], opponent_positions[pos_xmyp])
                else:
                    toggle_xmyp = False

            if toggle_xmym:
                if xm >= 0 and ym >= 0:
                    toggle_xmym, allowed_moves[pos_xmym] = self.is_blocked(
                        own_positions[pos_xmym], opponent_positions[pos_xmym])
                else:
                    toggle_xmym = False

        allowed_moves_coordinates = torch.nonzero(allowed_moves)
        allowed_moves = check_if_is_check(
            self, state, allowed_moves_coordinates, player, 2)

        return allowed_moves

    def get_allowed_rook_moves(self, state, player, position):
        return get_allowed_queen_moves(self, state, player, position, is_rook=True)

    def get_allowed_bishop_moves(self, state, player, position):
        return get_allowed_queen_moves(self, state, player, position, is_bishop=True)

    def get_allowed_knight_moves(self, state, player, position):
        own_board = state.get_player_positions(self, player)
        base = torch.tensor([
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0]
        ])

        allowed_moves = torch.conv(base, self.coordinate_to_point(position))
        available_spaces = abs(own_board - 1)
        allowed_moves *= available_spaces
        allowed_moves_coordinates = torch.nonzero(allowed_moves)

        allowed_moves_coordinates = torch.nonzero(allowed_moves)
        allowed_moves = check_if_is_check(
            self, state, allowed_moves_coordinates, player, 4)

    def get_allowed_pawn_moves(self, state, player, position):
        allowed_moves = torch.zeros((8, 8))
        if player == -1:
            allowed_moves[position[0], position[1] + 1] = 1
            if y_position == 1:
                allowed_moves[position[0], position[1] + 2] = 1

        else:
            if y_position == 6:

    def get_queen_move_pattern():
        return torch.tensor([
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        ])

    def get_rook_move_pattern():
        return torch.tensor([
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        ])

    def get_bishop_move_pattern():
        return torch.tensor([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ])

    def get_knight_move_pattern():
        return torch.tensor([
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0]
        ])

    def get_pawn_move_pattern():
        if state.get_player_color(player) == 0:
            return torch.tensor([
                [1, 1, 1],
                [0, 0, 0],
                [0, 0, 0]])

        else:
            return torch.tensor([
                [0, 0, 0],
                [0, 0, 0],
                [1, 1, 1]])
