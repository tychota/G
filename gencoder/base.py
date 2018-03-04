from gboard.gstate import GState
from gtypes.gpoint import GPoint


class GEncoder:
    def name(self):
        """Used for loading an encoder by name"""
        raise NotImplementedError()

    def encode(self, game_state: GState):
        """Turn a Go board into a numeric data"""
        raise NotImplementedError()

    def encode_point(self, point: GPoint):
        """Turn a Go board point into an integer index"""
        raise NotImplementedError()

    def decode_point_index(self, index):
        """Turn an integer index back into a Go board point"""
        raise NotImplementedError()

    def num_points(self):
        """Number of points on the board, i.e. board width times board height"""
        raise NotImplementedError()

    def shape(self):
        """Shape of the encoded board structure"""
        raise NotImplementedError()
