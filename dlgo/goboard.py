import copy
from typing import Collection, Dict, Optional, Union, Tuple, List, FrozenSet
from dlgo.gotypes import Player, Point
from dlgo import zobrist


class Move():
    def __init__(self, point: Point = None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point: Point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)


class GoString():
    def __init__(self, color: Player, stones: Collection[Point], liberties: Collection[Point]):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, go_string: 'GoString'):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        combined_liberties = (self.liberties | go_string.liberties) - combined_stones
        return GoString(self.color, combined_stones, combined_liberties)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other: object):
        if not isinstance(other, GoString):
            return False
        return self.color == other.color and self.stones == other.stones and self.liberties == other.liberties

    def __deepcopy__(self, memodict={}):
        return GoString(self.color, self.stones, copy.deepcopy(self.liberties))


class Board():
    def __init__(self, num_rows, nums_cols):
        self.num_rows = num_rows
        self.num_cols = nums_cols
        self._grid: Dict[Point, Optional[GoString]] = {}
        self._hash = zobrist.EMPTY_BOARD

    def place_stone(self, player: Player, point: Point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_gostrings_same_color: List[GoString] = []
        adjacent_gostrings_other_color: List[GoString] = []
        liberties: List[Point] = []

        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_gostring: Optional[GoString] = self._grid.get(neighbor)
            if neighbor_gostring is None:
                liberties.append(neighbor)
            elif neighbor_gostring.color == player:
                if neighbor_gostring not in adjacent_gostrings_same_color:
                    adjacent_gostrings_same_color.append(neighbor_gostring)
            else:
                if neighbor_gostring not in adjacent_gostrings_other_color:
                    adjacent_gostrings_other_color.append(neighbor_gostring)

        new_gostring = GoString(player, [point], liberties)
        for gostring_same_color in adjacent_gostrings_same_color:
            new_gostring = new_gostring.merged_with(gostring_same_color)
        for new_gostring_point in new_gostring.stones:
            self._grid[new_gostring_point] = new_gostring

        self._hash ^= zobrist.HASH_CODE[point, player]

        replacement = adjacent_gostrings_other_color.without_liberty(point)
        if replacement.num_liberties:
            self._replace_string(adjacent_gostrings_other_color.without_liberty(point))
        else:
            self._remove_string(adjacent_gostrings_other_color)

    def _replace_string(self, new_string):
        for point in new_string.stones:
            self._grid[point] = new_string

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
            self._grid[point] = None

        self._hash ^= zobrist.HASH_CODE[point, string.color]

    def is_on_grid(self, point: Point):
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point: Point) -> Player:
        gostring = self._grid.get(point)
        if gostring is None:
            return None
        return gostring.color

    def get_go_string(self, point: Point) -> Optional[GoString]:
        gostring = self._grid.get(point)
        if gostring is None:
            return None
        return gostring

    def __deepcopy__(self, memodict={}):
        copied = Board(self.num_rows, self.num_cols)
        # Can do a shallow copy b/c the dictionary maps tuples
        # (immutable) to GoStrings (also immutable)
        copied._grid = copy.copy(self._grid)
        copied._hash = self._hash
        return copied

    def zobrist_hash(self):
        return self._hash


class GameState():
    def __init__(self, board: Board, next_player: Player, previous_state: Optional['GameState'], move: Optional[Move]):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_state
        if self.previous_state is None:
            self.previous_states: FrozenSet[Tuple[Player, int]] = frozenset()
        else:
            self.previous_states = frozenset(self.previous_state.previous_states
                                             | {(self.previous_state.next_player,
                                                 self.previous_state.board.zobrist_hash())})
        self.last_move = move

    @property
    def situation(self):
        return (self.next_player, self.board)

    def apply_move(self, move: Move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size: Union[int, Tuple[int, int]]):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_over(self) -> bool:
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        if self.previous_state is None:
            return False
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def is_move_self_capture(self, player: Player, move: Move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_gostring = next_board.get_go_string(move.point)
        if new_gostring is None:
            return False
        return new_gostring.num_liberties == 0

    def does_move_violate_ko(self, player: Player, move: Move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move: Move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        if self.board.get(move.point) is not None:
            return False
        if self.is_move_self_capture(self.next_player, move):
            return False
        if self.does_move_violate_ko(self.next_player, move):
            return False
        return True
