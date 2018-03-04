from collections import namedtuple


class GPoint(namedtuple('Point', 'row col')):
    """A point is a namedtuple of row and column

    https://docs.python.org/3.6/library/collections.html#collections.namedtuple
    """
    def neighbours(self):
        """Return the neighbours of a single point

        Used for calculating the liberties of a go string
        """
        return [
            GPoint(self.row - 1, self.col),
            GPoint(self.row + 1, self.col),
            GPoint(self.row, self.col - 1),
            GPoint(self.row, self.col + 1),
        ]
