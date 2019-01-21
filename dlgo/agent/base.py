from dlgo.goboard_fast import Move


class Agent:
    def select_move(self, game_state) -> Move:
        raise NotImplementedError()
