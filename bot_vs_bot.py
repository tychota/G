from __future__ import print_function

import h5py

from dlgo.agent.naive import RandomBot
from dlgo.agent.predict import load_prediction_agent
from dlgo.goboard_fast import GameState
from dlgo.gotypes import Player
from dlgo.scoring import compute_game_result
from dlgo.utils import print_board, print_move


def main():
    board_size = 19
    game_state = GameState.new_game(board_size)
    bots = {
        Player.black: load_prediction_agent(h5py.File("./agents/deep_bot.h5", "r")),
        Player.white: RandomBot(),
    }
    while not game_state.is_over():
        # time.sleep(0.3)

        # print(chr(27) + "[2J")
        print_board(game_state.board)
        bot_move = bots[game_state.next_player].select_move(game_state)
        print_move(game_state.next_player, bot_move)
        game_state = game_state.apply_move(bot_move)
    print(game_state.winner())
    print(compute_game_result(game_state))


if __name__ == '__main__':
    main()
