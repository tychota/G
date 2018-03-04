import time

from gagent.gagent_naive import GAgentRandom
from gboard.gstate import GState
from gtypes.gplayer import GPlayer
from utils.display import print_board, print_move


def main():
    board_size = 9
    game = GState.new_game(board_size)
    bots = {
        GPlayer.black: GAgentRandom(),
        GPlayer.white: GAgentRandom(),
    }
    while not game.is_over():
        time.sleep(0.3)
        print(chr(27) + "[2J")
        print_board(game.gboard)
        bot_move = bots[game.next_gplayer].select_move(game)
        print_move(game.next_gplayer, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()