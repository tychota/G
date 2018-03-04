import six
from unittest import TestCase

from gboard.gboard import GBoard
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint


class TestGBoard(TestCase):
    def test_capture(self):
        board = GBoard(19, 19)
        board.place_stone(GPlayer.black, GPoint(2, 2))
        board.place_stone(GPlayer.white, GPoint(1, 2))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 2)))
        board.place_stone(GPlayer.white, GPoint(2, 1))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 2)))
        board.place_stone(GPlayer.white, GPoint(2, 3))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 2)))
        board.place_stone(GPlayer.white, GPoint(3, 2))
        self.assertIsNone(board.get(GPoint(2, 2)))

    def test_capture_two_stones(self):
        board = GBoard(19, 19)
        board.place_stone(GPlayer.black, GPoint(2, 2))
        board.place_stone(GPlayer.black, GPoint(2, 3))
        board.place_stone(GPlayer.white, GPoint(1, 2))
        board.place_stone(GPlayer.white, GPoint(1, 3))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 2)))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 3)))
        board.place_stone(GPlayer.white, GPoint(3, 2))
        board.place_stone(GPlayer.white, GPoint(3, 3))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 2)))
        self.assertEqual(GPlayer.black, board.get(GPoint(2, 3)))
        board.place_stone(GPlayer.white, GPoint(2, 1))
        board.place_stone(GPlayer.white, GPoint(2, 4))
        self.assertIsNone(board.get(GPoint(2, 2)))
        self.assertIsNone(board.get(GPoint(2, 3)))

    def test_capture_is_not_suicide(self):
        board = GBoard(19, 19)
        board.place_stone(GPlayer.black, GPoint(1, 1))
        board.place_stone(GPlayer.black, GPoint(2, 2))
        board.place_stone(GPlayer.black, GPoint(1, 3))
        board.place_stone(GPlayer.white, GPoint(2, 1))
        board.place_stone(GPlayer.white, GPoint(1, 2))
        self.assertIsNone(board.get(GPoint(1, 1)))
        self.assertEqual(GPlayer.white, board.get(GPoint(2, 1)))
        self.assertEqual(GPlayer.white, board.get(GPoint(1, 2)))

    def test_remove_liberties(self):
        board = GBoard(5, 5)
        board.place_stone(GPlayer.black, GPoint(3, 3))
        board.place_stone(GPlayer.white, GPoint(2, 2))
        white_string = board.get_gstring(GPoint(2, 2))
        six.assertCountEqual(
            self,
            [GPoint(2, 3), GPoint(2, 1), GPoint(1, 2), GPoint(3, 2)],
            white_string.liberties)
        board.place_stone(GPlayer.black, GPoint(3, 2))
        white_string = board.get_gstring(GPoint(2, 2))
        six.assertCountEqual(
            self,
            [GPoint(2, 3), GPoint(2, 1), GPoint(1, 2)],
            white_string.liberties)

    def test_empty_triangle(self):
        board = GBoard(5, 5)
        board.place_stone(GPlayer.black, GPoint(1, 1))
        board.place_stone(GPlayer.black, GPoint(1, 2))
        board.place_stone(GPlayer.black, GPoint(2, 2))
        board.place_stone(GPlayer.white, GPoint(2, 1))

        black_string = board.get_gstring(GPoint(1, 1))
        six.assertCountEqual(
            self,
            [GPoint(3, 2), GPoint(2, 3), GPoint(1, 3)],
            black_string.liberties)
