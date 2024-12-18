import re
import time
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
        grid_path[pos] = (dist, px, py)
        if target and pos == target:
            break
        for dx, dy in dxy:
            nx, ny = cx + dx, cy + dy
            next_grid_entry = grid.get((nx, ny))
            if next_grid_entry is not None and next_grid_entry != wall and (nx, ny) not in visited:
                heapq.heappush(to_visit, (dist + 1, nx, ny, cx, cy))
    return grid_path


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    w = h = param[0]
    first_loop = param[1]
    start = (0, 0)
    target = (w - 1, h - 1)

    grid = {}
    for y in range(h):
        for x in range(w):
            grid[(x, y)] = '.'

    inp = []
    for y, line in enumerate(lines):
        inp.append(nums(line))

    for idx, (cx, cy) in enumerate(inp):
        if idx == first_loop:
            path = determine_grid_path(start, grid, target)
            p1 = path[target][0]
        grid[(cx, cy)] = '#'
        if idx > first_loop:
            path = determine_grid_path(start, grid, target)
            if target not in path:
                # print(idx, cx, cy)
                p2 = "{:d},{:d}".format(cx, cy)
                break

    return p1, p2


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, (7, 12)],
        ['data.txt',    'real data    ', True,  False, (71, 1024)],
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
