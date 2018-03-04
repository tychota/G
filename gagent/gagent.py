import random
from typing import List

import numpy as np

from gagent.helper import is_point_an_eye
from gboard.gmove import GMove
from gboard.gstate import GState
from gtypes.gpoint import GPoint


class GAgent:
    def select_move(self, game_state: GState):
        raise NotImplementedError()


class GAgentRandom(GAgent):
    def __init__(self):
        self.dim = None
        self.point_cache: List[GPoint] = []

    def _update_cache(self, dim: (int, int)):
        self.dim = dim
        rows, cols = dim
        self.point_cache = []
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                self.point_cache.append(GPoint(row=r, col=c))

    def select_move(self, game_state: GState):
        dim = (game_state.gboard.num_rows, game_state.gboard.num_cols)
        if dim != self.dim:
            self._update_cache(dim)

        idx = np.arange(len(self.point_cache))
        np.random.shuffle(idx)

        for i in idx:
            p = self.point_cache[i]
            if game_state.is_valid_move(GMove.play(p)) and \
                    not is_point_an_eye(game_state.gboard, p, game_state.next_gplayer):
                return GMove.play(p)
        return GMove.pass_turn()
