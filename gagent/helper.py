from gboard.gboard import GBoard
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint


def is_point_an_eye(gboard: GBoard, gpoint: GPoint, color: GPlayer):
    # Eye is by definition an empty point
    if gboard.get(gpoint) is not None:
        return False
    # It is not an eye where there is mixed stone
    for neighbour in gpoint.neighbours():
        if gboard.is_on_grid(neighbour):
            neighbour_color = gboard.get(neighbour)
            if neighbour_color != color:
                return False
    # We have to control at least 3 corners for the eye to be settled on the middle of the board
    # On the edge, we must control every corner
    friendly_corners = 0
    off_board_corners = 0
    corners = [
        GPoint(gpoint.row - 1, gpoint.col - 1),
        GPoint(gpoint.row - 1, gpoint.col + 1),
        GPoint(gpoint.row + 1, gpoint.col - 1),
        GPoint(gpoint.row + 1, gpoint.col + 1),
    ]
    for corner in corners:
        if gboard.is_on_grid(corner):
            corner_color = gboard.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1

    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3
