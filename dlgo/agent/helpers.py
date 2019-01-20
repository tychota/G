from dlgo.gotypes import Point, Player
from dlgo.goboard_slow import Board


# this ignore falsey life eyes: https://senseis.xmp.net/?FalseEyeLife
def is_point_an_eye(board: Board, point: Point, color: Player):
    if board.get(point) is not None:
        return False
    # all adjacent neighbor must contains friendly stones
    for neighbor in point.neightbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1)
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    # point is on edge or corner
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    # point is on edge or corner
    return friendly_corners >= 3


__all__ = ["is_point_an_eye"]
