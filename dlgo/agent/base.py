from dlgo.goboard_slow import Move


class Agent:
    def select_move(self, game_state) -> Move:
        raise NotImplementedError()
