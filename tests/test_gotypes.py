import pytest
from dlgo.gotypes import Player, Point


class TestPlayer:
    def test_other_correct(self):
        player = Player.black
        assert player.other is Player.white

    def test_other_error(self):
        player = None
        with pytest.raises(AttributeError):
            player.other


class TestPoint:
    def test_point_correct(self):
        point = Point(1, 2)
        assert point.row is 1
        assert point.col is 2

    def test_point_error(self):
        with pytest.raises(TypeError):
            Point(1)

    def test_neighbor(self):
        point = Point(3, 4)
        neighbors = point.neightbors()

        expected = [Point(row=2, col=4), Point(row=4, col=4), Point(row=3, col=3), Point(row=3, col=5)]

        assert all([a == b for a, b in zip(neighbors, expected)])
