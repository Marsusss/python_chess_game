import copy

import torch

import utils.check_utils as check_utils


class Board:
    def __init__(self, player_colors, board=None):
        # I want to define _board as a pure 4x8x8 tensor for later operations
        # I am sacrificing fast interpretability and visualization to save later
        # Computation power when it needs to be trained on. I only add an extra
        # unnecessary dimension, the id dimension for tracking purposes necessary
        # to track pawn transformations.
        if board is None:
            self._board = torch.tensor(
                [
                    [
                        [3, 5, 4, 2, 1, 4, 5, 3],  # black pieces
                        [6, 6, 6, 6, 6, 6, 6, 6],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [6, 6, 6, 6, 6, 6, 6, 6],
                        [3, 5, 4, 2, 1, 4, 5, 3],  # white pieces
                    ],
                    [
                        [2, 2, 2, 2, 2, 2, 2, 2],  # black color
                        [2, 2, 2, 2, 2, 2, 2, 2],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],  # white color
                    ],
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],  # black states
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],  # white states
                    ],
                    [
                        [1, 2, 3, 4, 5, 6, 7, 8],  # black ids
                        [9, 10, 11, 12, 13, 14, 15, 16],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [17, 18, 19, 20, 21, 22, 23, 24],
                        [25, 26, 27, 28, 29, 30, 31, 32],  # white ids
                    ],
                ],
                dtype=torch.uint8,
            )
        else:
            self._board = board

        self.player_colors = player_colors

        check_utils.check_is_instance("board_0", self._board, torch.Tensor)
        if self._board.dtype != torch.uint8:
            raise TypeError(
                f"_board must be a Tensor of dtype uint8, got Tensor of dtype"
                f" {self._board.dtype}"
            )

        check_utils.check_is_instance("player_colors", player_colors, list)

        player_color_count = len(self.player_colors)
        if player_color_count < 2:
            raise ValueError(
                f"player_colors must have at least 2 colors, got {player_color_count}"
            )

        king_bins = self._board[0, :, :] == 1
        if torch.sum(king_bins) != player_color_count:
            raise ValueError(
                f"There must be as many kings ({torch.sum(king_bins)}) "
                f"as player_colors"
            )
        if (
            len(torch.unique_consecutive(self._board[1, :, :][king_bins]) - 1)
            != player_color_count
        ):
            raise ValueError(
                f"All kings {sum(king_bins)} must be of different color, "
                f"but got only {len(torch.unique(self._board[1,:,:][king_bins]))} "
                f"consecutive distinct"
            )

        if len(torch.unique(self._board[1, :, :])) - 1 != player_color_count:
            raise ValueError(
                f"The number of colors in player_colors {len(self.player_colors)}"
                f" must be the same as the number of colors on the board_0 "
                f"{len(torch.unique(self._board[1,:, :])) - 1}"
            )
        if self._board.shape[0] != 4:
            raise TypeError(
                f"The board_0 must have 4 layers, got {self._board.shape[0]}"
            )
        if min(self._board.shape[1:]) < 3:
            raise TypeError(
                f"The board_0 must be at least 3x3, got {self._board.shape[1:]}"
            )
        if max(self._board.shape[1:]) > 20:
            raise TypeError(
                f"The board_0 must be at most 20x20, got {self._board.shape[1:]}"
            )

        player_color_ids = torch.unique(self._board[1, :, :][self._board[1, :, :] != 0])
        self.player_color_id_to_color = dict(zip(player_color_ids, self.player_colors))

        alphabet = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
        ]
        self.letter_to_column = {
            letter: i for i, letter in enumerate(alphabet[: self._board.shape[2]])
        }
        self.letters = self.letter_to_column.keys()
        self.board_shape = self._board.shape

    def __copy__(self):
        new_copy = Board(player_colors=self.player_colors, board=self._board)
        return new_copy

    def __deepcopy__(self, memodict={}):
        new_copy = Board(
            player_colors=copy.deepcopy(self.player_colors), board=self._board.clone()
        )
        return new_copy

    def __getitem__(self, coordinates):
        if isinstance(coordinates, str):
            return self.get_piece_by_string(coordinates)

        return self._board[:, coordinates[0], coordinates[1]]

    def __str__(self):
        return self.board_as_string()

    def __repr__(self):
        return str(self)

    def string_to_coordinate(self, coordinate_string):
        if (
            len(coordinate_string) != 2
            or not coordinate_string[0].isalpha()
            or not coordinate_string[1].isdigit()
        ):
            raise TypeError(
                f"String coordinates must be in the format '<letter><int>', got "
                f"{coordinate_string}"
            )

        column_letter = coordinate_string[0]
        if column_letter not in self.letters:
            raise KeyError(f"Letter must be in {self.letters}, got {column_letter}")

        coordinate = (
            int(coordinate_string[1]) - 1,
            self.letter_to_column[column_letter],
        )

        return coordinate

    def board_as_string(self):
        return str(self._board)

    def get_board(self):
        return self._board

    def get_piece(self, coordinate):
        return self[coordinate]

    def get_piece_by_string(self, coordinate_string):
        coordinate = self.string_to_coordinate(coordinate_string)
        return self.get_piece(coordinate)

    def move_piece(self, old_coordinate, new_coordinate):
        for coordinate in [old_coordinate, new_coordinate]:
            for i, index in enumerate(coordinate):
                check_utils.check_is_index(index, self.board_shape[i + 1])

        if torch.equal(self[old_coordinate], torch.tensor([0, 0, 0, 0])):
            raise ValueError(
                f"Expected board[{old_coordinate}] to be non-empty, got "
                f"{self[old_coordinate]}"
            )

        self._board[:, new_coordinate[0], new_coordinate[1]] = self[old_coordinate]
        self._board[:, old_coordinate[0], old_coordinate[1]] = 0

    def is_similar_to(self, other):
        if self.player_colors != other.player_colors:
            return False
        if self.board_shape != other.board_shape:
            return False
        return True
