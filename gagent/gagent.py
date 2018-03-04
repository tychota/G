import math
from typing import List

import numpy as np

from gagent.helper import is_point_an_eye
from gboard.gmove import GMove
from gboard.gstate import GState
from gsearch.mcts.node import MCTSNode
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint
from gutils.display import STONE_TO_CHAR


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


class GAgentMCTS(GAgent):
    def __init__(self, num_rounds, temperature):
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state: GState) -> GMove:
        root: MCTSNode = MCTSNode(game_state)

        for i in range(self.num_rounds):
            mnode: MCTSNode = root
            while (not mnode.can_add_child()) and (not mnode.is_terminal()):
                mnode = self.select_child(mnode)

            if mnode.can_add_child():
                mnode = mnode.add_random_child()

            winner = self.simulate_random_game(mnode.gstate)
            print(STONE_TO_CHAR[winner], end='', flush=True)

            # Propagate the change from the winner to the tree
            while mnode is not None:
                mnode.record_win(winner)
                mnode = mnode.mparent
        print("")
        scored_moves = [
            (child.winning_pct(game_state.next_gplayer), child.gmove.gpoint, child.num_rollouts)
            for child in root.mchildren
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('%s - %.3f (%d)' % (m, s, n))

        best_move = None
        best_pct = -1.0
        for mchild in root.mchildren:
            child_pct = mchild.winning_pct(game_state.next_gplayer)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = mchild.gmove
        print('Select move %s with win pct %.3f' % (best_move.gpoint, best_pct))
        return best_move

    def select_child(self, mnode: MCTSNode) -> MCTSNode:
        total_rollouts = sum(child.num_rollouts for child in mnode.mchildren)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None

        # Loop over each child.
        for child in mnode.mchildren:
            # Calculate the UCT score.
            win_percentage = child.winning_pct(mnode.gstate.next_gplayer)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            if uct_score > best_score:
                best_score = uct_score
                best_child = child

        return best_child

    @staticmethod
    def simulate_random_game(game: GState):
        bots = {
            GPlayer.black: GAgentRandom(),
            GPlayer.white: GAgentRandom(),
        }
        while not game.is_over():
            bot_move = bots[game.next_gplayer].select_move(game)
            game = game.apply_move(bot_move)
        return game.winner()
