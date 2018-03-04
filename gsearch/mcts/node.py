import random
from typing import TypeVar, Optional

import math

from gboard.gmove import GMove
from gboard.gstate import GState
from gtypes.gplayer import GPlayer

T = TypeVar('T', bound='GState')


class MCTSNode:
    """A Node of the monte-carlo tree search"""
    def __init__(self, gstate: GState, mparent: Optional[T] = None, gmove: GMove = None):
        self.gstate = gstate
        self.gmove = gmove

        self.win_counts = {
            GPlayer.black: 0,
            GPlayer.white: 0,
        }
        self.num_rollouts = 0

        self.mchildren = []
        self.mparent = mparent
        self.unvisited_gmoves = gstate.legal_moves()

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_gmoves) - 1)

        new_gmove = self.unvisited_gmoves.pop(index)
        new_game_state = self.gstate.apply_move(new_gmove)

        new_mnode = MCTSNode(new_game_state, self, new_gmove)
        self.mchildren.append(new_mnode)

        return new_mnode

    def record_win(self, winner: GPlayer):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_gmoves) > 0

    def is_terminal(self):
        return self.gstate.is_over()

    def winning_pct(self, gplayer: GPlayer):
        return float(self.win_counts[gplayer]) / float(self.num_rollouts)
