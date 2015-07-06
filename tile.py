#!/usr/bin/python2

from collections import namedtuple
import sys


Coord = namedtuple('Coord', ['x', 'y'])


def ascii_to_coords (s):
    ret = []
    for y, line in enumerate(s.splitlines()):
        for x, char in enumerate(line):
            if char == '*':
                ret.append(Coord(x, -y))
            elif char != ' ':
                raise ValueError('Only spaces and asterisks allowed.')
    return frozenset(ret)


COORD_MAP = {k: ascii_to_coords(v) for k, v in {
        'I': '****',

        'O': '**\n' + \
             '**',

        'T': ' * \n' + \
             '***',

        'S': ' **\n' + \
             '**',

        'Z': '**\n' + \
             ' **',

        'J': '*\n' + \
             '***',

        'L': '  *\n' + \
             '***'
    }.items()
}


def get_coords (piece, orientation, dx, dy, memo={}):
    args = (piece, orientation, dx, dy)
    if args in memo: return memo[args]
    coords = COORD_MAP[piece]
    for i in xrange(orientation % 4):
        coords = [
            Coord(-y, x) for x, y in coords
        ]
    minx = min(c.x for c in coords)
    miny = min(c.y for c in coords)
    ret = frozenset([
        Coord(coord.x+dx-minx, coord.y+dy-miny) for coord in coords
    ])
    memo[args] = ret
    return ret


def draw (width, height, filled, coords):
    xs = [c.x for c in filled | coords]
    ys = [c.y for c in filled | coords]
    minx = min(min(xs), 0)
    maxx = max(max(xs), width)
    miny = min(min(ys), 0)
    maxy = max(max(ys), height)
    def char (c):
        valid = True
        if c.x < 0 or c.x >= width or \
            c.y < 0 or c.y >= height: valid = False
        if c in coords:
            if valid: return 'O '
            return '# '
        if c in filled:
            if valid: return '* '
            return 'X '
        if valid: return '. '
        return '  '
    rows = []
    for y in xrange(maxy, miny-1, -1):
        row = []
        rows.append(row)
        for x in xrange(minx, maxx+1):
            row.append(char(Coord(x, y)))
    return '\n'.join(''.join(row) for row in rows)


def solve_recurse (width, height, board, piece, pieces, filled,
    memo, debug=False):
    if filled in memo: return
    memo.add(filled)
    for orientation in xrange(4):
        for y in xrange(height):
            for x in xrange(width):
                coords = get_coords(piece, orientation, x, y)
                # Check that all coords are within the board.
                if coords & board != coords: continue
                # Check that coords don't overlap.
                if coords & filled: continue
                if debug and len(pieces) > debug:
                    print>>sys.stderr, len(pieces), piece, orientation, y, x
                    print>>sys.stderr, draw(width, height, filled, coords)
                #raw_input()
                # Check if we are finished.
                if not len(pieces):
                    # Return the successful piece/coord/orientation.
                    return frozenset([
                        (piece, Coord(x, y), orientation)
                    ])
                # Recurse.
                result = solve_recurse(
                    width, height,
                    board,
                    pieces[0], pieces[1:],
                    filled | coords,
                    memo=memo
                )
                # Check for success.
                if result is not None:
                    return result | frozenset([
                        (piece, Coord(x, y), orientation)
                    ])

          
def solve (width, height, pieces, debug=False):
    board = set()
    for y in xrange(height):
        for x in xrange(width):
            board.add(Coord(x, y))
    pieces = sorted(pieces)
    return solve_recurse(
        width,
        height,
        frozenset(board),
        pieces[0],
        tuple(pieces[1:]),
        frozenset(),
        memo=set(),
        debug=debug
    )


if __name__ == '__main__':
    print solve(8, 5, 'OOLJSZTTII', debug=5)