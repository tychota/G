from typing import List, Dict

from data import zobrist
from gboard.gstring import GString
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint


class GBoard:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid: Dict[GPoint, GString] = {}
        self._hash = zobrist.EMPTY_BOARD

    def place_stone(self, gplayer: GPlayer, gpoint: GPoint):
        # safety nets
        assert self.is_on_grid(gpoint)   # prevents playing outside of the board: illegal move
        assert self._grid.get(gpoint) is None  # prevents playing on existing stone: illegal move

        adjacent_same_color: List[GString] = []
        adjacent_opposite_color: List[GString] = []
        liberties: List[GPoint] = []

        for neighbour in gpoint.neighbours():
            # Do not explore the outside world: stay on board !
            if not self.is_on_grid(neighbour):
                continue
            # Get the value of the neighbour gpoint
            neighbour_gstring = self._grid.get(neighbour)
            # If none, it is a liberty
            if neighbour_gstring is None:
                liberties.append(neighbour)
            # Else, if it is is same color, it is part of our string
            elif neighbour_gstring.color == gplayer:
                if neighbour_gstring not in adjacent_same_color:
                    adjacent_same_color.append(neighbour_gstring)
            # Else, if it is the enemy
            else:
                if neighbour_gstring not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbour_gstring)

        new_gstring = GString(gplayer, [gpoint], liberties)

        # Merge adjacent string
        for same_color_gstring in adjacent_same_color:
            new_gstring = new_gstring.merged_with(same_color_gstring)
        # And update the grid for it
        for new_gstring_gpoint in new_gstring.stones:
            self._grid[new_gstring_gpoint] = new_gstring

        self._hash ^= zobrist.HASH_CODE[gpoint, gplayer]

        # Reduce liberties of adjacent opposite string
        for other_color_gstring in adjacent_opposite_color:
            replacement = other_color_gstring.without_liberty(gpoint)
            if replacement.num_liberties:
                self._replace_string(replacement)
            else:
                self._remove_string(other_color_gstring)

    def _replace_string(self, new_gstring: GString):
        """Extracted method to replace string: not mean to be used directly"""
        for point in new_gstring.stones:
            self._grid[point] = new_gstring

    def _remove_string(self, gstring: GString):
        """Extracted method to remove string: not mean to be used directly"""
        for gpoint in gstring.stones:
            for neighbour in gpoint.neighbours():
                neighbour_gstring = self._grid.get(neighbour)
                if neighbour_gstring is None:
                    continue
                # Removing string add liberties to neighbour string of opposite colour
                if neighbour_gstring is not gstring:
                    self._replace_string(neighbour_gstring.with_liberty(gpoint))
            self._grid[gpoint] = None

            self._hash ^= zobrist.HASH_CODE[gpoint, gstring.color]

    def zobrist_hash(self):
        return self._hash

    def is_on_grid(self, gpoint: GPoint) -> bool:
        return 1 <= gpoint.row <= self.num_rows and \
               1 <= gpoint.col <= self.num_cols

    def get(self, gpoint: GPoint):
        gstring = self._grid.get(gpoint)
        if gstring is None:
            return None
        return gstring.color

    def get_gstring(self, gpoint: GPoint):
        gstring = self._grid.get(gpoint)
        if gstring is None:
            return None
        return gstring
