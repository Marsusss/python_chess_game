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
    """

    def __init__(self, score=None):
        if score is None:
            self._score = {"p1": 0, "draw": 0, "p2": 0}
        else:
            self._score = score

        if not isinstance(self._score, dict):
            raise TypeError(f"score must be a dict, got {type(self._score)}")
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
            if not isinstance(value, int):
                raise TypeError(
                    f'score["{key}"] must be an integer, not {str(type(value))}.'
                )
            if value < 0:
                raise ValueError(
                    f'Error: score["{key}"] is {value}, should be at least 0'
                )

    def __getitem__(self, key):
        return self._score[key]

    def __setitem__(self, key, value):
        if key not in self._score:
            raise KeyError(
                f'Invalid key: "{key}". Only {self._score.keys()} are allowed.'
            )
        if not isinstance(value, int):
            raise TypeError(f"A score must be an integer, not {str(type(value))}.")
        if value < 0:
            raise ValueError(f'Error: score["{key}"] is {value}, should be at least 0')
        self._score[key] = value
