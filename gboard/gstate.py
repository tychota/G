import copy

from typing import TypeVar, Optional

from gboard.gboard import GBoard
from gboard.gmove import GMove
from gboard.gscoring import compute_game_result
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint

T = TypeVar('T', bound='GState')


class GState:
    """The Game State is a state machine that prevent wrong move"""
    def __init__(self, gboard: GBoard, next_gplayer: GPlayer, previous_gstate: T, gmove: Optional[GMove]):
        self.gboard = gboard
        self.next_gplayer = next_gplayer
        self.previous_gstate = previous_gstate
        if self.previous_gstate is None:
            self.previous_gstates = frozenset()
        else:
            self.previous_gstates = frozenset(
                previous_gstate.previous_gstates |
                {(previous_gstate.next_gplayer, previous_gstate.gboard.zobrist_hash())})
        self.last_gmove = gmove

    def apply_move(self, gmove: GMove):
        """Prevent a player playing twice"""
        if gmove.is_play:
            next_board = copy.deepcopy(self.gboard)
            next_board.place_stone(self.next_gplayer, gmove.gpoint)
        else:
            next_board = self.gboard
        return GState(next_board, self.next_gplayer.other, self, gmove)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = GBoard(*board_size)
        return GState(board, GPlayer.black, None, None)

    def is_move_self_capture(self, gplayer: GPlayer, gmove: GMove):
        """Prevent self capture"""
        if not gmove.is_play:
            return False
        return self.gboard.is_self_capture(gplayer, gmove.gpoint)

    @property
    def situation(self):
        return self.next_gplayer, self.gboard

    def does_move_violate_ko(self, gplayer: GPlayer, gmove: GMove):
        """Test Ko rule"""
        if not gmove.is_play:
            return False
        if not self.gboard.will_capture(gplayer, gmove.gpoint):
            return False

        next_gboard = copy.deepcopy(self.gboard)
        next_gboard.place_stone(gplayer, gmove.gpoint)
        next_situation = (gplayer.other, next_gboard.zobrist_hash())

        return next_situation in self.previous_gstates

    def is_valid_move(self, gmove: GMove):
        """Return true if the move is valid"""
        if self.is_over():
            return False
        if gmove.is_pass or gmove.is_resign:
            return True
        return (
            self.gboard.get(gmove.gpoint) is None and
            not self.is_move_self_capture(self.next_gplayer, gmove) and
            not self.does_move_violate_ko(self.next_gplayer, gmove))

    def is_over(self):
        """Handle the end of the game"""
        if self.last_gmove is None:
            return False
        if self.last_gmove.is_resign:
            return True
        second_last_move = self.previous_gstate.last_gmove
        if second_last_move is None:
            return False
        return self.last_gmove.is_pass and second_last_move.is_pass

    def legal_moves(self):
        if self.is_over():
            return []
        moves = []
        for row in range(1, self.gboard.num_rows + 1):
            for col in range(1, self.gboard.num_cols + 1):
                move = GMove.play(GPoint(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(GMove.pass_turn())
        moves.append(GMove.resign())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_gmove.is_resign:
            return self.next_gplayer
        game_result = compute_game_result(self)
        return game_result.winner
