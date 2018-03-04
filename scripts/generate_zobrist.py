import random

from gtypes.gplayer import GPlayer
from gtypes.gpoint import GPoint


def to_python(state):
    if state is None:
        return 'None'
    if state == GPlayer.black:
        return GPlayer.black
    return GPlayer.white

MAX63 = 0x7fffffffffffffff

table = {}
empty_board = 0
for row in range(1, 20):
    for col in range(1, 20):
        for state in (None, GPlayer.black, GPlayer.white):
            code = random.randint(0, MAX63)
            table[GPoint(row, col), state] = code
            if state is None:
                empty_board ^= code

print('from .gotypes import Player, Point')
print('')
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print('')
print('HASH_CODE = {')
for (pt, state), hash_code in table.items():
    print('    (%r, %s): %r,' % (pt, to_python(state), hash_code))
print('}')
print('')
print('EMPTY_BOARD = %d' % (empty_board,))
