import time
from copy import deepcopy
import pyperclip


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    starts = []
    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            v = int(ch)
            grid[(x, y)] = v
            if v == 0:
                starts.append((x, y))

    for (sx, sy) in starts:
        peaks = set()
        paths = find_paths(grid, sx, sy, [], peaks)
        p1 += len(peaks)
        p2 += len(paths)

    return p1, p2


def find_paths(grid, cx, cy, path, peaks):
    cv = grid[(cx, cy)]
    path.append((cx, cy, cv))
    if cv == 9:
        peaks.add((cx, cy))
        return [path]

    paths = []
    for dx, dy in dxy:
        nx, ny = cx + dx, cy + dy
        if (nx, ny) in grid:
            nv = grid[(nx, ny)]
            if cv + 1 == nv:
                paths.extend(find_paths(grid, nx, ny, deepcopy(path), peaks))

    return paths


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
