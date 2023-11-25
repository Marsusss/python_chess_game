from modules.game_log import Game_log
from utils.utils import check_utils


class Game_log_list:
    def __init__(self, player_ids=None):
        if player_ids is None:
            self.player_ids = ["white", "black"]
        else:
            self.player_ids = player_ids

        self.log_list = []

    def __getitem__(self, index):
        return self.get_log(index)

    def __str__(self):
        return self.print_list()

    def update_list(self, game_log):
        check_utils.check_is_instance("game_log", game_log, Game_log)
        self.log_list.append(game_log)

    def print_list(self):
        output = f"players: {self.player_ids}\n"
        for game_log in self.log_list:
            output += (f"game number: {game_log.game_number}, player colors by id "
                       f"{game_log.player_colors}\n")
        return output

    def get_log(self, index):
        check_utils.check_is_index(index, len(self.log_list))
        return self.log_list[index]

    def get_player_ids(self):
        return self.player_ids

    def get_log_list(self):
        return self.log_list
