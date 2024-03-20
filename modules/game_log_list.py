import utils.check_utils as check_utils
from modules.game_log import GameLog


class GameLogList:
    def __init__(self, player_colors=None):
        if player_colors is None:
            self.player_colors = ["white", "black"]
        else:
            self.player_colors = player_colors

        check_utils.check_is_iterable_of_unique_elements_with_length(
            "player_colors", self.player_colors, list, min_length=2
        )

        self.log_list = []

    def __getitem__(self, index):
        return self.log_list[index]

    def __len__(self):
        return len(self.log_list)

    def __iter__(self):
        return iter(self.log_list)

    def __str__(self):
        return self.list_as_string()

    def __repr__(self):
        return str(self)

    def update_list(self, game_log):
        check_utils.check_is_instance("game_log", game_log, GameLog)
        check_utils.check_is_iterable_of_unique_elements_with_length(
            "game_log.player_id_to_color",
            game_log.player_id_to_color,
            dict,
            len(self.player_colors),
        )
        for color in game_log.player_id_to_color.values():
            if color not in self.player_colors:
                raise ValueError(
                    f"{color} is not in player_colors " f"{self.player_colors}"
                )

        self.log_list.append(game_log)

    def list_as_string(self):
        output = f"players: {self.player_colors}\n"
        for game_log in self.log_list:
            output += (
                f"game number: {game_log.game_number}, player colors by id "
                f"{game_log.player_id_to_color}\n"
            )
        return output

    def get_log(self, index):
        check_utils.check_is_index(index, len(self.log_list))
        return self[index]

    def get_player_colors(self):
        return self.player_colors

    def get_log_list(self):
        return self.log_list
