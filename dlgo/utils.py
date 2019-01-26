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
    print('=> %s %s' % (player.name, move))


def print_board(board: Board):
    table = [[""] + list(COLS[:board.num_cols])]
    for row in range(board.num_rows, 0, -1):
        line = [str(row)]
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        table.append(line)
    print(AsciiTable(table).table)


def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return Point(row=row, col=col)


def coords_from_point(point):
    return '%s%d' % (
        COLS[point.col - 1],
        point.row
    )
