# score = torch.tensor([p1_win, remis, p2_win]), result is a 1/0 for each of these
# white pieces: king = 1, queen = 2, castle = 3, bishop = 4, knight = 5, pawn = 6
# player is 0 or 1
# player color 1 is white, -1 is black
import torch
import numpy

initial_board = torch.tensor([
[0,  0,  0,  0, -1,  0,  0,  0], #black
[0,  0,  0,  0,  0,  0,  0,  0],
[0,  0,  0,  0,  0,  0,  0,  0],
[0,  0,  0,  0,  0,  0,  0,  0],
[0,  0,  0,  0,  0,  0,  0,  0],
[0,  0,  0,  0,  0,  0,  0,  0],
[0,  0,  0,  0,  0,  0,  0,  0],
[0,  0,  0,  0,  1,  0,  0,  0]  #white
])

class state:
    def __init__(self, score = torch.tensor([0, 0, 0]), turn = 0, player_colors = [1, -1], game_count = 0,
    board = initial_board):
        self.board = board
        self.score = score
        self.turn_number = turn
        self.play_turn = 1
        self.player_colors = player_colors
        self.game_count = game_count

    def update_positions(self, prev_pos, new_pos):
        self.board[new_pos] = self.board[prev_pos]
        self.board[prev_pos] = 0

    def update_score(self, result):
        self.score += result

    def update_turn_number(self):
        self.turn_number += 1
        self.player_turn *= -1

    def update_game_count(self):
        self.game_count += 1

    def update_player_colors(self):
        self.player_colors.reverse()

    def game_end(self, result):
        self.update_game_count()
        self.update_score(result)
        self.update_player_colors()
        self.reset()

    def reset(self):
        self.board = initial_board
        self.turn_number = 0
        self.player_turn = 1

    def get_player_color(self, player):
        return self.player_colors[player]

    def get_player_positions(self, player):
        player_color = self.get_player_color(player)
        return self.board * player_color > 0

    def get_player_pieces_and_coordinates(self, player):
        positions = self.get_player_positions(self, player)
        return self.board[positions], torch.nonzero(positions)
