import argparse
import numpy as np
from pathlib import Path

from gencoder import get_encoder_by_name
from gboard.gstate import GState
from gagent.gagent import GAgentMCTS
from gencoder.base import GEncoder
from gutils.display import print_board, print_move


def generate_game(board_size, rounds, max_moves, temperature):
    boards = []
    moves = []

    encoder: GEncoder = get_encoder_by_name('betago', board_size)
    game = GState.new_game(board_size)
    bot = GAgentMCTS(rounds, temperature)

    num_moves = 0

    while not game.is_over():
        print_board(game.gboard)
        gmove = bot.select_move(game)

        if gmove.is_play:
            boards.append(encoder.encode(game))

            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(gmove.gpoint)] = 1
            moves.append(move_one_hot)

        print_move(game.next_gplayer, gmove)
        game = game.apply_move(gmove)
        num_moves += 1

        if num_moves > max_moves:
            break
    try:
        print('Player %s win with %.2f' % (game.winner().name, game.winning_margin()))
    except AttributeError:
        pass
    return np.array(boards), np.array(moves)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-b', type=int, default=3)
    parser.add_argument('--rounds', '-r', type=int, default=100)
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--max-moves', '-m', type=int, default=60, help='Max moves per game.')
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out', default="data/features.npy")
    parser.add_argument('--move-out', default="data/label.npy")
    args = parser.parse_args()

    if Path(args.board_out).is_file() and Path(args.move_out).is_file():
        Xs = [np.load(args.board_out)]
        ys = [np.load(args.move_out)]
    else:
        Xs = []
        ys = []


    for i in range(args.num_games):
        print('########################')
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        print('########################')
        X, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        Xs.append(X)
        ys.append(y)
        Xt = np.concatenate(Xs)
        yt = np.concatenate(ys)
        np.save(args.board_out, Xt)
        np.save(args.move_out, yt)

if __name__:
    main()
