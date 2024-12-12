import time
from collections import *
import pyperclip


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]

#        NORTH -> CLOCKWISE with diagonals
ddxy = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            grid[(x, y)] = ch

    h = len(lines)
    w = len(lines[0])

    p1, p2 = 0, 0
    seen = set()
    for y in range(h):
        for x in range(w):
            ch = grid[(x, y)]
            contains, perimeter, corners = determine_perimeter_and_corners(grid, x, y, ch, seen)
            p1 += contains * perimeter
            p2 += contains * corners

    return p1, p2


def grid_get(grid, x, y):
    # return a char which is not in input data, if (x, y) not in grid,
    # in order to treat also outer grid border as perimeter
    return grid.get((x, y), '-')


def determine_perimeter_and_corners(grid, x, y, ch, seen):
    if (x, y) in seen:
        return 0, 0, 0

    q = deque()
    q.append((x, y))

    contains = 0
    perimeter = 0
    corners = set()
    while q:
        cx, cy = q.popleft()
        if (cx, cy) in seen:
            continue
        seen.add((cx, cy))

        contains += 1
        for dx, dy in dxy:
            nx, ny = cx + dx, cy + dy
            if grid_get(grid, nx, ny) != ch:
                perimeter += 1
            else:
                if (nx, ny) not in seen:
                    q.append((nx, ny))

        s = ['-' for _ in range(len(ddxy))]
        for idx, (dx, dy) in enumerate(ddxy):
            nx, ny = cx + dx, cy + dy
            if grid_get(grid, nx, ny) == ch:
                s[idx] = ch

        # outside corners, don't check the middle index against != ch, because there
        # could be another area of the same char, which is considered unconnected
        if s[0] != ch and s[2] != ch:
            corners.add((cx, cy, 'ONE'))
        if s[2] != ch and s[4] != ch:
            corners.add((cx, cy, 'OSE'))
        if s[4] != ch and s[6] != ch:
            corners.add((cx, cy, 'OSW'))
        if s[6] != ch and s[0] != ch:
            corners.add((cx, cy, 'ONW'))

        # inside corners
        if s[0] == ch and s[1] != ch and s[2] == ch:
            corners.add((cx, cy, 'INE'))
        if s[2] == ch and s[3] != ch and s[4] == ch:
            corners.add((cx, cy, 'ISE'))
        if s[4] == ch and s[5] != ch and s[6] == ch:
            corners.add((cx, cy, 'ISW'))
        if s[6] == ch and s[7] != ch and s[0] == ch:
            corners.add((cx, cy, 'INW'))

    # print(ch, contains, len(corners), corners)

    return contains, perimeter, len(corners)


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, None],
        ['data.txt',    'real data    ', True,  False, None],
    ]

    for filename, description, use_data, verbose, param in input_data_list:
        if use_data:
            start = time.time()
            p1, p2 = solve_puzzle('data/' + filename, param, verbose)
            end = time.time()
            printc(p1)
            if p2:
                printc(p2)
            else:
                print(p2)
            print("%s \tin %d ms" % (description, round(1000 * (end - start), 2)))


if __name__ == '__main__':
    main()
