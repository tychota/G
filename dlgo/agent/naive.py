import random
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_fast import Move, GameState
from dlgo.gotypes import Point


class RandomBot(Agent):
    def select_move(self, game_state: GameState):
        candidates = []
        for row_index in range(1, game_state.board.num_rows + 1):
            for col_index in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=row_index, col=col_index)
                is_valid_move = game_state.is_valid_move(Move.play(candidate))
                is_not_stupid_move = not is_point_an_eye(game_state.board, candidate, game_state.next_player)
                if is_valid_move and is_not_stupid_move:
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))

