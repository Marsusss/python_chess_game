import utils.check_utils as check_utils


class Score:
    """
    A class to represent a score in a two-player game.

    ...

    Attributes
    ----------
    _score : dict
        a dictionary representing the score for each player and a draw

    Methods
    -------
    __getitem__(key)
        Returns the score for the given key.
    __setitem__(key, value)
        Sets the score for the given key to the given value.
    keys()
        Returns the keys of the score dictionary.
    values()
        Returns the values of the score dictionary.
    update_score(winner)
        Increments the score of the given winner by 1.
    """

    def __init__(self, score=None):
        if score is None:
            self._score = {"p1": 0, "draw": 0, "p2": 0}
        else:
            self._score = score

        check_utils.check_is_instance("score", self._score, dict)
        if "draw" not in self._score.keys():
            raise ValueError(
                f'score must include a "draw" key, got dict with keys: '
                f"{self._score.keys()}"
            )
        if len(self._score) != 3:
            raise ValueError(
                f"score must be a dict of length 3: 2 players and a draw option, got "
                f"dict of length {len(self._score)}"
            )
        for key, value in self._score.items():
            check_utils.check_is_non_negative_int(f'score["{key}"]', value)

    def __getitem__(self, key):
        return self._score[key]

    def __setitem__(self, key, value):
        if key not in self._score:
            raise KeyError(
                f'Invalid key: "{key}". Only {self._score.keys()} are allowed.'
            )
        check_utils.check_is_non_negative_int(f'score["{key}"]', value)
        self._score[key] = value

    def keys(self):
        return self._score.keys()

    def values(self):
        return self._score.values()

    def update_score(self, winner):
        if winner not in self._score:
            raise KeyError(
                f'Invalid key: "{winner}". Only {self._score.keys()} are allowed.'
            )
        self._score[winner] += 1
