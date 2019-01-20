import copy
from typing import List, Mapping
from dlgo.gotypes import Player, Point


class Move():
    def __init__(self, point: Point = None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point: Point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls, point):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)


class GoString():
    def __init__(self, color: Player, stones: List[Point], liberties: List[Point]):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remvove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string: GoString):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        combined_liberties = (self.liberties | go_string.liberties) - combined_stones
        return GoString(self.color, combined_stones, combined_liberties)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other: GoString):
        if not isinstance(other, GoString):
            return False
        return self.color == other.color and self.stones == other.stones and self.liberties == other.liberties


class Board():
    def __init__(self, num_rows, nums_cols):
        self.num_rows = num_rows
        self.num_cols = nums_cols
        self._grid: Mapping[Point, GoString] = {}

    def place_stone(self, player: Player, point: Point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_gostrings_same_color: List[GoString] = []
        adjacent_gostrings_other_color: List[GoString] = []
        liberties: List[Point] = []

        for neighbor in point.neightbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_gostring: GoString = self._grid.get(neighbor)
            if neighbor_gostring is None:
                liberties.append(neighbor)
            elif neighbor_gostring.color == player:
                if neighbor_gostring not in adjacent_gostrings_same_color:
                    adjacent_gostrings_same_color.append(neighbor_gostring)
            else:
                if neighbor_gostring not in adjacent_gostrings_other_color:
                    adjacent_gostrings_other_color.append(neighbor_gostring)

        new_gostring = GoString(player, [point], liberties)
        for gostring_same_color in adjacent_gostrings_same_color:
            new_gostring = new_gostring.merged_with(gostring_same_color)
        for new_gostring_point in new_gostring.stones:
            self._grid[new_gostring_point] = new_gostring
        for gostring_other_color in adjacent_gostrings_other_color:
            gostring_other_color.remvove_liberty(point)
        for gostring_other_color in adjacent_gostrings_other_color:
            if gostring_other_color.num_liberties == 0:
                self._remove_string(gostring_other_color)

    def is_on_grid(self, point: Point):
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point: Point) -> Player:
        string = self._grid.get(point)
        if string == None:
            return None
        return string.color

    def get_go_string(self, point: Point) -> GoString:
        string = self._grid.get(point)
        if string == None:
            return None
        return string

    def _remove_string(self, gostring: GoString):
        for point in gostring.stones:
            for neighbor in point.neightbors():
                neighbor_gostring: GoString = self._grid.get(neighbor)
                if neighbor_gostring is None:
                    continue
                if neighbor_gostring is not gostring:
                    neighbor_gostring.add_liberty(point)
            self._grid[point] = None