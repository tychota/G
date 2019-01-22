import math
import progressbar

from dlgo.agent.base import Agent
from dlgo.agent.naive import RandomBot
from dlgo.goboard_fast import Move, GameState
from dlgo.gotypes import Player
from dlgo.mcts.mcts import MCTSNode


def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration


class MCTSAgent(Agent):
    def __init__(self, num_rounds, temperature):
        Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state: GameState) -> Move:
        root = MCTSNode(game_state)

        with progressbar.ProgressBar(max_value=self.num_rounds) as bar:
            for i in range(self.num_rounds):
                node = root
                while not node.can_add_child() and not node.is_terminal():
                    node = self.select_child(node)

                if node.can_add_child():
                    node = node.add_random_child()

                winner = self.simulate_random_game(node.game_state)
                while node is not None:
                    node.record_win(winner)
                    node = node.parent
                bar.update(i)

        scored_moves = [
            (child.winning_pct(game_state.next_player), child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('++ Move %s - win pct %.3f (%d games)' % (m, s, n))

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_pct(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        return best_move

    def select_child(self, node: MCTSNode):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = -1
        best_child = None
        for child in node.children:
            score = uct_score(total_rollouts, child.num_rollouts, child.winning_pct(node.game_state.next_player),
                              self.temperature)
            if score > best_score:
                best_score = score
                best_child = child
        # print('-- UCT for move %s: %s' % (best_child.move, best_score))
        return best_child

    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.black: RandomBot(),
            Player.white: RandomBot(),
        }
        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)
        return game.winner()
