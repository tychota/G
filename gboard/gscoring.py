from collections import namedtuple
from typing import List, Dict, Union

from gboard.gboard import GBoard
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint


class GTerritory:
    def __init__(self, gterritory_map):
        self.num_black_gterritory = 0
        self.num_white_gterritory = 0
        self.num_black_gstones = 0
        self.num_white_gstones = 0
        self.num_gdame = 0  # https://senseis.xmp.net/?Dame
        self.gdame_points: List[GPoint] = []
        for point, status in gterritory_map.items():
            if status == GPlayer.black:
                self.num_black_gstones += 1
            elif status == GPlayer.white:
                self.num_white_gstones += 1
            elif status == 'territory_b':
                self.num_black_gterritory += 1
            elif status == 'territory_w':
                self.num_white_gterritory += 1
            elif status == 'dame':
                self.num_gdame += 1
                self.gdame_points.append(point)


class GameResult(namedtuple('GameResult', 'b w komi')):
    @property
    def winner(self):
        if self.b > self.w + self.komi:
            return GPlayer.black
        return GPlayer.white

    @property
    def winning_margin(self):
        w = self.w + self.komi
        return abs(self.b - w)

    def __str__(self):
        w = self.w + self.komi
        if self.b > w:
            return 'B+%.1f' % (self.b - w,)
        return 'W+%.1f' % (w - self.b,)


def evaluate_territory(gboard: GBoard):
    """Map a board into territory and dame.

    Any points that are completely surrounded by a single color are
    counted as territory; it makes no attempt to identify even
    trivially dead groups.
    """
    status: Dict[GPoint, Union[GPlayer, str]] = {}
    for r in range(1, gboard.num_rows + 1):
        for c in range(1, gboard.num_cols + 1):
            p = GPoint(row=r, col=c)
            if p in status:
                # Already visited this as part of a different group.
                continue
            stone = gboard.get(p)
            if stone is not None:
                # It's a stone.
                status[p] = gboard.get(p)
            else:
                group, neighbors = _collect_region(p, gboard)
                if len(neighbors) == 1:
                    # Completely surrounded by black or white.
                    neighbor_stone = neighbors.pop()
                    stone_str = 'b' if neighbor_stone == GPlayer.black else 'w'
                    fill_with = 'territory_' + stone_str
                else:
                    # Dame.
                    fill_with = 'dame'
                for pos in group:
                    status[pos] = fill_with
    return GTerritory(status)


def _collect_region(start_pos: GPoint, board: GBoard, visited: bool = None):
    """Find the contiguous section of a board containing a point. Also
    identify all the boundary points.
    """
    if visited is None:
        visited: Dict[GPoint, bool] = {}
    if start_pos in visited:
        return [], set()
    all_points = [start_pos]
    all_borders = set()
    visited[start_pos] = True

    here = board.get(start_pos)
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for delta_r, delta_c in deltas:
        next_p = GPoint(row=start_pos.row + delta_r, col=start_pos.col + delta_c)
        if not board.is_on_grid(next_p):
            continue
        neighbor = board.get(next_p)
        if neighbor == here:
            points, borders = _collect_region(next_p, board, visited)
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders


def compute_game_result(game_state, komi=7.5):
    territory = evaluate_territory(game_state.gboard)
    return GameResult(
        territory.num_black_gterritory + territory.num_black_gstones,
        territory.num_white_gterritory + territory.num_white_gstones,
        komi=komi
    )
