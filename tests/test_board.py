import copy
import unittest

from modules.board import Board
from modules.chess_piece import ChessPiece
from modules.king import King
from modules.pawn import Pawn


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.player_colors = ["white", "black"]
        self.board = Board(player_colors=self.player_colors)

    def test_init(self):
        # Test player colors
        self.assertEqual(self.board.player_colors, self.player_colors)

        # Test board dimensions
        self.assertEqual(len(self.board), 8)
        for row in self.board:
            self.assertEqual(len(row), 8)

        # Test pieces
        self.assertIsInstance(self.board[0, 4], King)
        self.assertIsInstance(self.board[7, 4], King)
        for i in range(8):
            self.assertIsInstance(self.board[1, i], Pawn)
            self.assertIsInstance(self.board[6, i], Pawn)

        self.assertEqual(self.board.king_positions, {"white": (0, 4), "black": (7, 4)})

        self.board = Board(
            self.player_colors,
            [
                [
                    {"type": "king", "color": "white"},
                    {"type": "pawn", "color": "white", "forward_direction": "down"},
                    None,
                ],
                [
                    {"type": "pawn", "color": "white", "forward_direction": "down"},
                    [],
                    [],
                ],
                [[], [], {"type": "pawn", "color": "black", "forward_direction": "up"}],
                [
                    [],
                    {"type": "pawn", "color": "black", "forward_direction": "up"},
                    {"type": "king", "color": "black"},
                ],
            ],
            board_by_config=True,
        )

        self.assertEqual(
            self.board._board,
            [
                [King((0, 0), "white", 0), Pawn((0, 1), "white", 1, "down"), None],
                [Pawn((1, 0), "white", 2, "down"), None, None],
                [None, None, Pawn((2, 2), "black", 3, "up")],
                [None, Pawn((3, 1), "black", 4, "up"), King((3, 2), "black", 5)],
            ],
        )

    def test_eq(self):
        other_board = Board(player_colors=self.player_colors)
        self.assertEqual(self.board, other_board)

        other_board[0, 0] = Pawn((0, 0), "white", 8, "down")
        self.assertNotEqual(self.board, other_board)

        other_board[0, 0] = None
        self.assertEqual(self.board, other_board)

        other_board[1, 0] = Pawn((1, 0), "white", 20, "up")
        self.assertNotEqual(self.board, other_board)

        other_board.player_colors = ["black", "white"]
        self.assertNotEqual(self.board, other_board)

    def test_neq(self):
        other_board = Board(player_colors=self.player_colors)
        self.assertNotEqual(self.board == other_board, self.board != other_board)

        other_board[0, 0] = Pawn((0, 0), "white", 8, "down")
        self.assertNotEqual(self.board == other_board, self.board != other_board)

        other_board[0, 0] = None
        self.assertNotEqual(self.board == other_board, self.board != other_board)

        other_board[1, 0] = Pawn((1, 0), "white", 20, "up")
        self.assertNotEqual(self.board == other_board, self.board != other_board)

        other_board.player_colors = ["black", "white"]
        self.assertNotEqual(self.board == other_board, self.board != other_board)

    def test_board_as_string(self):
        board_string = self.board.board_as_string()
        # Check that the string starts with a newline
        self.assertEqual(board_string[0], "\n")

        # Split the string into lines
        lines = board_string.split("\n")[1:-1]

        # Check that there are 8 lines (for 8 rows of the board)
        self.assertEqual(len(lines), 8)

        for line in lines:
            # Split the line into squares
            squares = line[:-1].split(" ")
            self.assertEqual(len(squares), 8)

            for square in squares:  # Can't explain
                self.assertTrue(
                    square == "O"
                    or (
                        square[:5] in ChessPiece.color_codes.values()
                        and square[5] in ChessPiece.symbol_schema.values()
                        and (square[6:] == ChessPiece.color_codes["reset"])
                        or square[7:] == ChessPiece.color_codes["reset"]
                    )
                )

    def test_display(self):
        try:
            self.board.display()
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__} unexpectedly!")

    def test_getitem(self):
        self.assertEqual(self.board[:, :], self.board._board[:][:])
        self.assertEqual(self.board["a1"], self.board._board[0][0])
        self.assertEqual(self.board[0, 0], self.board._board[0][0])
        self.assertEqual(self.board[0], self.board._board[0])
        self.assertEqual(self.board[2:7], self.board._board[2:7])

    def test_setitem(self):
        # Test setting a single item
        piece = Pawn((3, 3), "black", 40, "up")
        self.board[1, 2] = piece
        self.assertEqual(self.board[1, 2], piece)

        # Test setting a slice
        self.board[1:3, 2:4] = piece
        self.assertEqual(self.board[1:3, 2:4], [[piece, piece], [piece, piece]])

        self.board[1:3, 2:4] = None
        self.assertEqual(self.board[1:3, 2:4], [[None, None], [None, None]])

        self.board[1] = [
            Pawn((1, i), self.board.player_colors[0], 8 + i, "down") for i in range(8)
        ]
        for i, element in enumerate(self.board[1, :]):
            self.assertEqual(
                element, Pawn((1, i), self.board.player_colors[0], 8 + i, "down")
            )

    def test_str(self):
        self.assertEqual(str(self.board), self.board.board_as_string())

    def test_repr(self):
        self.assertEqual(repr(self.board), str(self.board))

    def test_get_board(self):
        self.assertEqual(self.board.get_board(), self.board._board)

    def test_get_piece(self):
        self.assertEqual(self.board.get_piece((0, 0)), self.board[0, 0])

    def test_get_piece_by_string(self):
        self.assertEqual(self.board.get_piece_by_string("a1"), self.board[0, 0])

    def test_is_colors_pieces(self):
        is_whites = self.board.is_colors_pieces("white")
        for i, row in enumerate(is_whites):
            for j, column in enumerate(row):
                if not column:
                    if self.board[i, j] is not None:
                        self.assertNotEqual(self.board[i, j]["color"], "white")
                elif column:
                    self.assertEqual(self.board[i, j]["color"], "white")
                else:
                    raise ValueError("Invalid value in is_whites")

    def test_move_piece(self):
        # Test not allowed move
        old_coordinate = (0, 4)
        new_coordinate = (1, 4)
        with self.assertRaises(ValueError):
            self.board.move_piece(old_coordinate, new_coordinate)

        # Test not on board
        new_coordinate = (-1, 0)
        with self.assertRaises(ValueError):
            self.board.move_piece(old_coordinate, new_coordinate)

        # Test allowed move
        old_coordinate = (1, 0)
        new_coordinate = (2, 0)
        pawn = self.board[old_coordinate]
        self.board.move_piece(old_coordinate, new_coordinate)
        self.assertEqual(self.board[new_coordinate], pawn)
        self.assertEqual(self.board[old_coordinate], None)
        self.assertEqual(self.board.board_cache, {})

        # Test en passant
        self.board[2, 1] = Pawn((2, 1), "black", 40, "up")
        self.board[2, 1]["state"]["is_en_passant_able"] = True

        self.board.move_piece((2, 0), (3, 1))
        self.assertEqual(self.board[3, 1], pawn)
        self.assertEqual(self.board[2, 1], None)

        # Test change king_position
        print(self.board)
        self.board[1, 4] = None
        self.board.move_piece((0, 4), (1, 4))
        self.assertEqual(self.board.king_positions["white"], (1, 4))
        self.assertEqual(self.board.board_cache, {})

        # Test building board cache on reversible move
        self.board.move_piece((0, 3), (0, 4))
        self.assertEqual(
            self.board.board_cache,
            {(tuple(tuple(row) for row in self.board), self.board[0, 4]["color"]): 1},
        )

        # Test clearing board_cache on kill
        self.board[0, 3] = Pawn((0, 3), "black", 41, "up")
        self.board.move_piece((0, 4), (0, 3))
        self.assertEqual(self.board.board_cache, {})

    def test_update_board_cache(self):
        # Test update on move
        self.board.update_board_cache(
            self.board[0, 4], copy.deepcopy(self.board[0, 4]), self.board, False
        )
        self.assertEqual(
            self.board.board_cache,
            {(tuple(tuple(row) for row in self.board), self.board[0, 4]["color"]): 1},
        )

        # Test count equal boards
        self.board.update_board_cache(
            self.board[0, 4], copy.deepcopy(self.board[0, 4]), self.board, False
        )
        self.assertEqual(
            self.board.board_cache,
            {(tuple(tuple(row) for row in self.board), self.board[0, 4]["color"]): 2},
        )
        self.assertEqual(self.board.threefold_repetition, False)

        # Test threefold repetition
        self.board.update_board_cache(
            self.board[0, 4], copy.deepcopy(self.board[0, 4]), self.board, False
        )
        self.assertEqual(
            self.board.board_cache,
            {(tuple(tuple(row) for row in self.board), self.board[0, 4]["color"]): 3},
        )
        self.assertEqual(self.board.threefold_repetition, True)

        # Test add different board to cache
        old_board = copy.deepcopy(self.board)
        self.board[1, 0] = None
        self.board.update_board_cache(
            self.board[0, 4], copy.deepcopy(self.board[0, 4]), self.board, False
        )
        self.assertEqual(len(self.board.board_cache), 2)
        self.assertEqual(
            self.board.board_cache[
                (tuple(tuple(row) for row in old_board), self.board[0, 4]["color"])
            ],
            3,
        )
        self.assertEqual(
            self.board.board_cache[
                (tuple(tuple(row) for row in self.board), self.board[0, 4]["color"])
            ],
            1,
        )
        self.assertEqual(self.board.threefold_repetition, True)

        # Test clear cache on pawn move
        self.board.update_board_cache(
            self.board[1, 1], copy.deepcopy(self.board[1, 1]), self.board, False
        )
        self.assertEqual(self.board.board_cache, {})

        self.board.update_board_cache(
            self.board[0, 4], copy.deepcopy(self.board[0, 4]), self.board, False
        )
        self.board.update_board_cache(
            self.board[7, 4], copy.deepcopy(self.board[7, 4]), self.board, False
        )

        self.assertEqual(
            self.board.board_cache,
            {
                (tuple(tuple(row) for row in self.board), self.board[0, 4]["color"]): 1,
                (tuple(tuple(row) for row in self.board), self.board[7, 4]["color"]): 1,
            },
        )

        with self.assertRaises(TypeError):
            self.board.update_board_cache(
                self.board[0, 4], copy.deepcopy(self.board[0, 4]), "not a board", False
            )

        with self.assertRaises(TypeError):
            self.board.update_board_cache(
                "not a chess piece", copy.deepcopy(self.board[0, 4]), self.board, False
            )

        with self.assertRaises(TypeError):
            self.board.update_board_cache(
                self.board[0, 4], "not a chess piece", self.board, False
            )

    def test_get_candidate_moves(self):
        candidate_moves = self.board.get_candidate_moves("white")
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is None or self.board[i, j]["color"] != "white":
                    self.assertEqual(candidate_moves[i][j], [])

                else:
                    self.assertEqual(
                        candidate_moves[i][j],
                        self.board[i, j].get_allowed_moves(self.board),
                    )

        with self.assertRaises(ValueError):
            self.board.get_candidate_moves("color not on board")

    def test_get_allowed_moves(self):
        self.assertEqual(
            self.board.get_allowed_moves(
                "white", self.board.get_candidate_moves("white")
            ),
            self.board.get_candidate_moves("white"),
        )

        self.board[1, 3] = Pawn((1, 3), "black", 40, "up")
        self.board[1, 3]["state"]["has_moved"] = True

        self.assertEqual(
            self.board.get_allowed_moves(
                "white", self.board.get_candidate_moves("white")
            ),
            [
                [[], [(1, 3)], [(1, 3)], [(1, 3)], [(1, 3)], [], [], []],
                [[], [], [], [], [], [], [], []],
                [[], [], [], [], [], [], [], []],
                [[], [], [], [], [], [], [], []],
                [[], [], [], [], [], [], [], []],
                [[], [], [], [], [], [], [], []],
                [[], [], [], [], [], [], [], []],
                [[], [], [], [], [], [], [], []],
            ],
        )

        with self.assertRaises(ValueError):
            self.board.get_allowed_moves(
                "color not on board", self.board.get_candidate_moves("white")
            )

    def test_is_check(self):
        self.assertFalse(self.board.is_check("white"))
        self.assertFalse(self.board.is_check("black"))

        self.board[1, 3] = Pawn((1, 3), "black", 40, "up")
        self.board[1, 3]["state"]["has_moved"] = True

        self.assertTrue(self.board.is_check("white"))
        self.assertFalse(self.board.is_check("black"))

        with self.assertRaises(ValueError):
            self.board.is_check("color not on board")

    def test_has_no_allowed(self):
        self.assertFalse(self.board.has_no_allowed_moves("white"))
        self.assertFalse(self.board.has_no_allowed_moves("black"))

        for column_idx in range(self.board.board_shape[1]):
            self.board[1, column_idx] = Pawn(
                (1, column_idx), "black", 40 + column_idx, "up"
            )
            self.board[1, column_idx]["state"]["has_moved"] = True
            self.board[2, column_idx] = Pawn(
                (2, column_idx), "black", 50 + column_idx, "up"
            )
            self.board[2, column_idx].position = (2, column_idx)

        self.assertTrue(self.board.has_no_allowed_moves("white"))

        with self.assertRaises(ValueError):
            self.board.has_no_allowed_moves("color not on board")

    def test_is_checkmate(self):
        self.assertFalse(self.board.is_checkmate("white"))
        self.assertFalse(self.board.is_checkmate("black"))

        self.board[1, 3] = Pawn((1, 3), "black", 40, "up")
        self.board[1, 3]["state"]["has_moved"] = True

        self.assertFalse(self.board.is_checkmate("white"))

        for column_idx in range(self.board.board_shape[1]):
            self.board[1, column_idx] = Pawn(
                (1, column_idx), "black", 40 + column_idx, "up"
            )
            self.board[1, column_idx]["state"]["has_moved"] = True
            self.board[2, column_idx] = Pawn(
                (2, column_idx), "black", 50 + column_idx, "up"
            )
            self.board[2, column_idx].position = (2, column_idx)

        self.assertTrue(self.board.is_checkmate("white"))

        with self.assertRaises(ValueError):
            self.board.is_checkmate("color not on board")

    def test_has_no_moves_and_is_not_check(self):
        self.assertFalse(self.board.has_no_allowed_moves_and_is_not_check("white"))
        self.assertFalse(self.board.has_no_allowed_moves_and_is_not_check("black"))

        for column_idx in range(self.board.board_shape[1]):
            self.board[1, column_idx] = Pawn(
                (1, column_idx), "black", 40 + column_idx, "up"
            )
            self.board[1, column_idx]["state"]["has_moved"] = True
            self.board[2, column_idx] = Pawn(
                (2, column_idx), "black", 50 + column_idx, "up"
            )
            self.board[2, column_idx].position = (2, column_idx)

        self.assertFalse(self.board.has_no_allowed_moves_and_is_not_check("white"))
        self.board[1, 3:6] = self.board[0, :4] = self.board[0, 5:] = None

        self.assertTrue(self.board.has_no_allowed_moves_and_is_not_check("white"))

        with self.assertRaises(ValueError):
            self.board.has_no_allowed_moves_and_is_not_check("color not on board")

    def test_copy(self):
        copied_board = copy.copy(self.board)
        self.assertEqual(copied_board.player_colors, self.board.player_colors)
        self.assertEqual(copied_board._board, self.board._board)
        self.assertIsNot(copied_board, self.board)
        self.assertIs(copied_board._board, self.board._board)

    def test_deepcopy(self):
        deepcopy_board = copy.deepcopy(self.board)
        self.assertIsNot(deepcopy_board, self.board)

        self.assertEqual(deepcopy_board.player_colors, self.board.player_colors)
        self.assertIsNot(deepcopy_board.player_colors, self.board.player_colors)
        self.assertEqual(deepcopy_board.board_shape, self.board.board_shape)
        self.assertEqual(deepcopy_board.letter_to_column, self.board.letter_to_column)
        self.assertEqual(deepcopy_board.letters, self.board.letters)

        self.assertIsNot(deepcopy_board._board[0][4], self.board._board[0][4])
        self.assertEqual(deepcopy_board._board[0][4].dict, self.board._board[0][4].dict)

    def test_is_occupied(self):
        for row in range(self.board.board_shape[0]):
            for column in range(self.board.board_shape[1]):
                if isinstance(self.board[row, column], ChessPiece):
                    self.assertTrue(self.board.is_occupied((row, column)))
                else:
                    self.assertFalse(self.board.is_occupied((row, column)))

        with self.assertRaises(ValueError):
            self.board.is_occupied((self.board.board_shape[0], 0))

    def test_is_on_board(self):
        self.assertTrue(self.board.is_on_board((0, 0)))
        self.assertFalse(self.board.is_on_board((self.board.board_shape[0], 0)))

    def test_is_on_board_and_occupied_by(self):
        position = (1, 0)
        color = "white"
        self.assertTrue(self.board.is_on_board_and_occupied_by(position, [color]))

        color = "black"
        self.assertFalse(self.board.is_on_board_and_occupied_by(position, [color]))

        colors = ["white", "black"]
        self.assertTrue(self.board.is_on_board_and_occupied_by(position, colors))

        position = (0, 0)
        self.assertFalse(self.board.is_on_board_and_occupied_by(position, [color]))
        self.assertFalse(self.board.is_on_board_and_occupied_by(position, colors))

        position = (self.board.board_shape[0], 0)
        self.assertEqual(
            self.board.is_on_board_and_occupied_by(position, [color]),
            self.board.is_on_board(position),
        )

        with self.assertRaises(TypeError):
            self.board.is_on_board_and_occupied_by((1, 0), "not a list")

        with self.assertRaises(TypeError):
            self.board.is_on_board_and_occupied_by("not a coordinate", colors)

        with self.assertRaises(ValueError):
            self.board.is_on_board_and_occupied_by((1, 0))

        with self.assertRaises(ValueError):
            self.board.is_on_board_and_occupied_by((1, 0), [])

    def test_is_similar_to(self):
        self.assertTrue(self.board.is_similar_to(Board(self.player_colors)))
        self.assertFalse(self.board.is_similar_to(Board(["red", "green"])))

        other_board = copy.deepcopy(self.board)
        self.assertTrue(self.board.is_similar_to(other_board))
        other_board.board_shape = (3, 3)
        self.assertFalse(self.board.is_similar_to(other_board))

        with self.assertRaises(TypeError):
            self.board.is_similar_to("not a board")

    def test_init_invalid_player_colors(self):
        with self.assertRaises(TypeError):
            Board(player_colors={})
        with self.assertRaises(ValueError):
            Board(player_colors=["w"])  # not enough player colors

    def test_init_invalid_board_shape(self):
        with self.assertRaises(ValueError):
            Board(
                player_colors=["w", "b"],
                board=[[None for _ in range(2)] for _ in range(2)],
            )  # too small
        with self.assertRaises(ValueError):
            Board(
                player_colors=["w", "b"],
                board=[[None for _ in range(2)] for _ in range(21)],
            )  # too large

    def test_getitem_invalid_coordinate(self):
        with self.assertRaises(IndexError):
            self.board[8, 8]  # out of bounds

        with self.assertRaises(TypeError):
            self.board["invalid"]  # invalid string coordinate

    def test_string_to_coordinate_invalid_string(self):
        with self.assertRaises(TypeError):
            self.board.string_to_coordinate("invalid")  # too long
        with self.assertRaises(KeyError):
            self.board.string_to_coordinate("z1")  # invalid letter

    def test_get_piece_as_list(self):
        with self.assertRaises(TypeError):
            self.board.get_piece_as_list(1)

        self.assertEqual([0, 6, 0], self.board.get_piece_as_list(None))

        pawn = Pawn((2, 1), "black", 40, "up")
        self.assertEqual(
            [
                self.board.player_colors.index(pawn["color"]),
                list(pawn.symbol_schema.keys()).index(pawn["type"]),
                0,
            ],
            self.board.get_piece_as_list(pawn),
        )

        pawn["state"]["has_moved"] = True
        pawn["state"]["is_en_passant_able"] = True
        self.assertEqual(
            [
                self.board.player_colors.index(pawn["color"]),
                list(pawn.symbol_schema.keys()).index(pawn["type"]),
                2,
            ],
            self.board.get_piece_as_list(pawn),
        )

        king = King((0, 0), "white", 1)
        self.assertEqual(
            [
                self.board.player_colors.index(king["color"]),
                list(king.symbol_schema.keys()).index(king["type"]),
                0,
            ],
            self.board.get_piece_as_list(king),
        )

    def test_update_board_as_list(self):
        position = (1, 0)
        color = "black"
        id = 1
        self.board[1, 0] = None
        self.board[2, 0] = Pawn(position, color, id, "up")
        self.board.update_board_as_list((1, 0), (2, 0))
        self.assertEqual([0, 6, 0], self.board.board_as_list[1][0])
        self.assertEqual([1, 5, 0], self.board.board_as_list[2][0])

        color = "white"
        self.board[2, 0] = King(position, color, id)
        self.board.update_board_as_list((1, 0), (2, 0))
        self.assertEqual([0, 6, 0], self.board.board_as_list[1][0])
        self.assertEqual([0, 0, 0], self.board.board_as_list[2][0])

    def test_save_board_as_img(self):
        self.board.save_board_as_img("somefile.png")
        # Check that the file was created
        success = False
        import os

        for file in os.listdir():
            if file == "somefile.png":
                success = True
                break

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
