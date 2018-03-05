import warnings
from typing import TypeVar


from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint

T = TypeVar('T', bound='String')


class GString:
    """A string in Go is a list of connected stone.

    Viewing the stones in the board in term of string helps implementing the logic and reduce the complexity
    """
    def __init__(self, color: GPlayer, stones, liberties):
        self.color = color
        self.stones = frozenset(stones)  # prevents duplicate
        self.liberties = frozenset(liberties)  # prevents duplicate

    def without_liberty(self, gpoint: GPoint):
        new_liberties = self.liberties - {gpoint}
        return GString(self.color, self.stones, new_liberties)

    def with_liberty(self, gpoint: GPoint):
        new_liberties = self.liberties | {gpoint}
        return GString(self.color, self.stones, new_liberties)

    def remove_liberty(self, gpoint: GPoint):
        """Remove the liberty at a certain point

        This happens for instance if the other player plays at this points"""
        warnings.warn("deprecated", DeprecationWarning)
        self.liberties = self.without_liberty(gpoint)

    def add_liberty(self, gpoint: GPoint):
        """Add liberties at a certain point

        This happens for instance when player extends the string by playing near or capture other player stone"""
        warnings.warn("deprecated", DeprecationWarning)
        self.liberties = self.with_liberty(gpoint)

    def merged_with(self, other_gstring: T):
        """merge two strings together

        This happen when a player connects two string by putting a stone in between
        """
        assert other_gstring.color == self.color
        combined_stones = self.stones | other_gstring.stones
        return GString(self.color, combined_stones, (self.liberties | other_gstring.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GString) and \
               self.color == other.color and \
               self.stones == other.stones and \
               self.liberties == other.liberties

    def __deepcopy__(self, memodict={}):
        return GString(self.color, self.stones, copy.deepcopy(self.liberties))
