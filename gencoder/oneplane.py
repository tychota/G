import numpy as np

from gboard.gstate import GState
from gencoder.base import GEncoder
from gtypes.gpoint import GPoint


class OnePlaneEncoder(GEncoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):  # <1>
        return 'oneplane'

    def encode(self, game_state: GState):
        board_matrix = np.zeros(self.shape())
        next_gplayer = game_state.next_gplayer
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = GPoint(row=r + 1, col=c + 1)
                gstring = game_state.gboard.get_gstring(p)
                if gstring is None:
                    continue
                if gstring.color == next_gplayer:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = -1
        return board_matrix

    def encode_point(self, point):
        return self.board_width * (point.row - 1) + (point.col - 1)

    def decode_point_index(self, index):
        row = index // self.board_width
        col = index % self.board_width
        return GPoint(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width



# tag::oneplane_create[]
def create(board_size):
    return OnePlaneEncoder(board_size)
