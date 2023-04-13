class Alignment:
    """
    LEFT = `0` or `l`
    MIDDLE = `~1` or `m`
    RIGHT = `~2` or `r`

    UP = `0` or `u`
    MIDDLE = `~1` or `m`
    DOWN = `~2` or `d`
    """

    LEFT = 0
    CENTRE = -667
    MIDDLE = -667
    RIGHT = -668

    UP = 0
    TOP = -666
    DOWN = -668
    BOTTOM = -668

    @staticmethod
    def from_tilde_string(string: str):
        return {"0": Alignment.LEFT, "1": Alignment.MIDDLE, "2": Alignment.RIGHT}[
            string[1]
        ]

    @staticmethod
    def from_direction_letter(string: str):
        return {
            "l": Alignment.LEFT,
            "m": Alignment.MIDDLE,
            "r": Alignment.RIGHT,
            "u": Alignment.UP,
            "d": Alignment.DOWN,
        }[string.lower()]
