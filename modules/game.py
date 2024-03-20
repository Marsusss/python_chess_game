import utils.check_utils as check_utils
from modules.board import Board
from modules.game_log import GameLog

# from modules.human_player import HumanPlayer
# from modules.ai_player import AiPlayer


class Game:
    def __init__(self, board=None, player_id_to_player_config=None):
        if player_id_to_player_config is None:
            self.player_id_to_player_config = {
                "p1": {"color": "white", "type": "ai", "model": "random"},
                "p2": {"color": "black", "type": "ai", "model": "random"},
            }
        else:
            check_utils.check_is_iterable_of_unique_elements_with_length(
                "player_id_to_player_config",
                player_id_to_player_config,
                dict,
                min_length=2,
                max_length=10,
            )
            for player_config in self.player_id_to_player_config.values():
                check_utils.check_is_iterable_of_unique_elements_with_length(
                    "player_config", player_config, dict, min_length=2, max_length=3
                )
            self.player_id_to_player_config = player_id_to_player_config

        self.player_ids = list(self.player_id_to_player_config.keys())
        self.player_id_to_color = {
            player_id: player_config["color"]
            for player_id, player_config in self.player_id_to_player_config.items()
        }

        self.player_id_to_player = {}
        # for player_id, player_config in self.player_id_to_player_config.items():
        #     if player_config["type"] == "human":
        #         self.player_id_to_player[player_id] = HumanPlayer(
        #             player_id, self.player_id_to_color[player_id]
        #         )
        #
        #     elif player_config["type"] == "ai":
        #         self.player_id_to_player[player_id] = AiPlayer(
        #             player_id,
        #             self.player_id_to_color[player_id],
        #         )
        #
        #     else:
        #         raise ValueError(
        #             f'Expected player_type to be in ["human", "ai"], got'
        #             f'{player_config["type"]}'
        #         )

        if board is None:
            self.board = Board(list(self.player_id_to_color.values()))
        else:
            check_utils.check_is_instance("board", board, Board)
            self.board = board

        # if len(self.board.player_colors) != len(self.player_id_to_player):
        #     print(self.player_id_to_player)
        #     raise ValueError(
        #         f"The number of player colors on the board "
        #         f"{len(self.board.player_colors)} must match the number of players "
        #         f"{len(self.player_id_to_player)}."
        #     )
        # for color in self.player_id_to_color.values():
        #     if color not in self.board.player_colors:
        #         raise ValueError(
        #             f"Expected players and board to have same colors, but got"
        #             f"{self.player_id_to_color.values()} and "
        #             f"{self.board.player_colors} respectively."
        #         )

        self.game_log = GameLog(self.player_id_to_color)
        self.player_count = len(self.player_id_to_player)
        self.turn_count = 0
        self.player_idx_turn = 0
        self.state = {"state": "in_progress", "winner": None}

    def __str__(self):
        return (
            f"Players: {self.player_id_to_player}\n Turn: {self.turn_count}\n "
            f"Current Player: "
            # f'{self.player_id_to_player[self.player_ids[self.player_idx_turn]]}\n '
            f"Board: {self.board}\n Game Log: {self.game_log}"
        )

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.state[item]

    def get_board(self):
        return self.board

    def get_game_log(self):
        return self.game_log

    def get_player_id_to_player(self):
        return self.player_id_to_player

    def get_game_state(self):
        return self.state

    def move_piece(self, player_id, start_pos, end_pos):
        if self.player_id_to_player[
            player_id
        ].get_color() != self.board.get_piece_color(start_pos):
            raise ValueError(
                f"Player {player_id} tried to move a piece of the wrong color"
            )

        self.board.move_piece(start_pos, end_pos)
        self.game_log.update_log(self.board)

    def get_player_move(self, player_id):
        start_pos, end_pos = self.player_id_to_player[player_id].get_move(self.board)
        return start_pos, end_pos

    def take_turn(self):
        player_id = self.player_ids[self.player_idx_turn]
        start_pos, end_pos = self.get_player_move(player_id)
        self.move_piece(player_id, start_pos, end_pos)
        self.turn_count += 1
        self.state = self.check_game_state(player_id)
        self.player_idx_turn = (self.player_idx_turn + 1) % self.player_count

    def play_game(self):
        while self.state["state"] == "in_progress":
            self.take_turn()

    def check_game_state(self, current_player_id):
        for player_id in self.player_ids:
            if player_id != current_player_id:
                if self.board.is_checkmate(self.player_id_to_color[player_id]):
                    return {"state": "checkmate", "winner": current_player_id}
            if self.board.is_stalemate(self.player_id_to_color[player_id]):
                return {"state": "stalemate", "winner": None}
        return {"state": "in_progress", "winner": None}
