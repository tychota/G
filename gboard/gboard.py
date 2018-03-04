from typing import List, Dict, Optional

from data import zobrist
from gboard.gstring import GString
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint

neighbour_tables = {}
corner_tables = {}


def init_neighbour_table(dim):
    rows, cols = dim
    new_table = {}
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            p = GPoint(row=r, col=c)
            full_neighbours = p.neighbours()
            true_neighbours = [
                n for n in full_neighbours
                if 1 <= n.row <= rows and 1 <= n.col <= cols]
            new_table[p] = true_neighbours
    neighbour_tables[dim] = new_table


def init_corner_table(dim):
    rows, cols = dim
    new_table = {}
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            p = GPoint(row=r, col=c)
            full_corners = [
                GPoint(row=p.row - 1, col=p.col - 1),
                GPoint(row=p.row - 1, col=p.col + 1),
                GPoint(row=p.row + 1, col=p.col - 1),
                GPoint(row=p.row + 1, col=p.col + 1),
            ]
            true_corners = [
                n for n in full_corners
                if 1 <= n.row <= rows and 1 <= n.col <= cols]
            new_table[p] = true_corners
    corner_tables[dim] = new_table


class GBoard:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid: Dict[GPoint, GString] = {}
        self._hash = zobrist.EMPTY_BOARD

        global neighbour_tables
        dim = (num_rows, num_cols)
        if dim not in neighbour_tables:
            init_neighbour_table(dim)
        if dim not in corner_tables:
            init_corner_table(dim)
        self.neighbour_table = neighbour_tables[dim]
        self.corner_table = corner_tables[dim]

    def neighbours(self, point):
        return self.neighbour_table[point]

    def corners(self, point):
        return self.corner_table[point]

    def place_stone(self, gplayer: GPlayer, gpoint: GPoint):
        # safety nets
        assert self.is_on_grid(gpoint)   # prevents playing outside of the board: illegal move
        assert self._grid.get(gpoint) is None  # prevents playing on existing stone: illegal move

        adjacent_same_color: List[GString] = []
        adjacent_opposite_color: List[GString] = []
        liberties: List[GPoint] = []

        for neighbour in self.neighbour_table[gpoint]:
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
            for neighbour in self.neighbour_table[gpoint]:
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

    def is_self_capture(self, player: GPlayer, point: GPoint) -> bool:
        friendly_strings: List[GString] = []
        for neighbour in self.neighbour_table[point]:
            neighbour_string = self._grid.get(neighbour)
            if neighbour_string is None:
                # This point has a liberty. Can't be self capture.
                return False
            elif neighbour_string.color == player:
                # Gather for later analysis.
                friendly_strings.append(neighbour_string)
            else:
                if neighbour_string.num_liberties == 1:
                    # This move is real capture, not a self capture.
                    return False
        if all(neighbour.num_liberties == 1 for neighbour in friendly_strings):
            return True
        return False

    def will_capture(self, player: GPlayer, point: GPoint) -> bool:
        for neighbour in self.neighbour_table[point]:
            neighbour_string = self._grid.get(neighbour)
            if neighbour_string is None:
                continue
            elif neighbour_string.color == player:
                continue
            else:
                if neighbour_string.num_liberties == 1:
                    # This move would capture.
                    return True
        return False

    def is_on_grid(self, gpoint: GPoint) -> bool:
        return 1 <= gpoint.row <= self.num_rows and \
               1 <= gpoint.col <= self.num_cols

    def get(self, gpoint: GPoint) -> Optional[GPlayer]:
        gstring = self._grid.get(gpoint)
        if gstring is None:
            return None
        return gstring.color

    def get_gstring(self, gpoint: GPoint) -> Optional[GString]:
        gstring = self._grid.get(gpoint)
        if gstring is None:
            return None
        return gstring
