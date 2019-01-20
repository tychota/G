import enum
from typing import List, NamedTuple
from collections import namedtuple


class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white


class Point(NamedTuple):
    row: int
    col: int

    def neightbors(self) -> List['Point']:
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
