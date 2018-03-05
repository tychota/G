from gtypes.gpoint import GPoint

COLS = 'ABCDEFGHJKLMNOPQRST'


class GMove:
    """A move represent the action of a player at some point.

    It can either be playing by placing a stone on board or passing or resigning
    """
    def __init__(self, gpoint: GPoint = None, is_pass: bool = False, is_resign: bool = False) -> None:
        assert (gpoint is not None) ^ is_pass ^ is_resign  # Safety net: ensure that move makes sense
        self.gpoint = gpoint
        self.is_play = (self.gpoint is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, gpoint):
        """Generate a play move: putting a stone on board"""
        return GMove(gpoint=gpoint)

    @classmethod
    def pass_turn(cls):
        """Generate a pass move"""
        return GMove(is_pass=True)

    @classmethod
    def resign(cls):
        """Generate a resign move"""
        return GMove(is_resign=True)

    def __str__(self):
        if self.is_pass:
            move_str = 'passes'
        elif self.is_resign:
            move_str = 'resigns'
        else:
            move_str = '%s%d' % (COLS[self.gpoint.col - 1], self.gpoint.row)
        return move_str
