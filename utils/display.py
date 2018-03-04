from gboard.gboard import GBoard
from gboard.gmove import GMove
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: '.',
    GPlayer.black: 'x',
    GPlayer.white: 'o',
}


def print_move(player: GPlayer, move: GMove):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.gpoint.col - 1], move.gpoint.row)
    print('%s %s' % (player, move_str))


def print_board(board: GBoard):
    for row in range(board.num_rows, 0, -1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(GPoint(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%d %s' % (row, ''.join(line)))
    print(' ' + COLS[:board.num_cols])