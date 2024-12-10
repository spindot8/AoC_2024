import time
from copy import deepcopy
import pyperclip
import heapq


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


# Determine all shortest distances within the grid from start position
# until either target position is reached or all reachable grid elements
# are processed. Grid elements which are walls ('#' by default) are not
# considered as being reachable.
# The result is a path grid (dict) which contains for every position from
# the original grid (or just until the target position was processed) the
# shortest distance to the start_pos and the x and y coordinate of each
# predecessor within the grid.
def determine_grid_path(start_pos, grid, target=None, wall='#'):
    grid_path = {}

    cx, cy = start_pos
    visited = set()
    to_visit = []
    heapq.heappush(to_visit, (0, cx, cy, cx, cy))
    while len(to_visit) > 0:
        dist, cx, cy, px, py = heapq.heappop(to_visit)
        pos = (cx, cy)
        if pos in visited:
            continue
        visited.add(pos)
        cv = grid[(cx, cy)]
        grid_path[pos] = (dist, px, py, cv)
        if target and pos == target:
            break
        for dx, dy in dxy:
            nx, ny = cx + dx, cy + dy
            next_grid_entry = grid.get((nx, ny))
            if next_grid_entry is not None and (nx, ny) not in visited:
                if cv + 1 == next_grid_entry:
                    heapq.heappush(to_visit, (dist + 1, nx, ny, cx, cy))
    return grid_path


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

    for start in starts:
        grid_path = determine_grid_path(start, grid)
        for k, v in grid_path.items():
            (dist, px, py, n) = v
            if n == 9:
                p1 += 1

    for (sx, sy) in starts:
        paths = find_paths(grid, sx, sy, [])
        p2 += len(paths)

    return p1, p2


def find_paths(grid, cx, cy, path):
    cv = grid[(cx, cy)]
    path.append((cx, cy, cv))
    if cv == 9:
        return [path]

    paths = []
    for dx, dy in dxy:
        nx, ny = cx + dx, cy + dy
        if (nx, ny) in grid:
            nv = grid[(nx, ny)]
            if cv+1 == nv:
                paths.extend(find_paths(grid, nx, ny, deepcopy(path)))

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
