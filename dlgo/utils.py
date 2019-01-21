from terminaltables import AsciiTable

from dlgo.goboard_fast import Board, Move
from dlgo.gotypes import Point, Player

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' ',
    Player.black: '●',
    Player.white: '◯',
}


def print_move(player: Player, move: Move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('=> %s %s' % (player.name, move_str))


def print_board(board: Board):
    table = [[""] + list(COLS[:board.num_cols])]
    for row in range(board.num_rows, 0, -1):
        line = [str(row)]
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        table.append(line)
    print(AsciiTable(table).table)
