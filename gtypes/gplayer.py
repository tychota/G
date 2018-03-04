import enum


class GPlayer(enum.Enum):
    """This enum is used to represent the player.

    Each case of the board can either be None (if no one plays) or Player.white / Player.black
    """
    black = 1
    white = 2

    @property
    def other(self):
        """Return the opposite player"""
        return GPlayer.black if self == GPlayer.white else GPlayer.white
