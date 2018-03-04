from gboard.gstate import GState


class GAgent:
    def select_move(self, game_state: GState):
        raise NotImplementedError()
