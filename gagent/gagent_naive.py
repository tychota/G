import random
from gagent.gagent_base import GAgent
from gagent.helper import is_point_an_eye
from gboard.gmove import GMove
from gboard.gstate import GState
from gtypes.gpoint import GPoint


class GAgentRandom(GAgent):
    def select_move(self, game_state: GState):
        candidates = []
        for r in range(1, game_state.gboard.num_rows + 1):
            for c in range(1, game_state.gboard.num_cols + 1):
                candidate = GPoint(row=r, col=c)
                if game_state.is_valid_move(GMove.play(candidate)) and \
                        not is_point_an_eye(game_state.gboard, candidate, game_state.next_gplayer):
                    candidates.append(candidate)
        if not candidates:
            return GMove.pass_turn()
        return GMove.play(random.choice(candidates))
