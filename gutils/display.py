from terminaltables import AsciiTable

from gboard.gboard import GBoard
from gboard.gmove import GMove
from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' ',
    GPlayer.black: '●',
    GPlayer.white: '◯',
}


def print_move(player: GPlayer, move: GMove):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.gpoint.col - 1], move.gpoint.row)
    print('=> %s %s' % (player.name, move_str))


def print_board(board: GBoard):
    table = [[""] + list(COLS[:board.num_cols])]
    for row in range(board.num_rows, 0, -1):
        line = [row]
        for col in range(1, board.num_cols + 1):
            stone = board.get(GPoint(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        table.append(line)
    print(AsciiTable(table).table)
