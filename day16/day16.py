import time
from collections import *
import pyperclip
import heapq


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def print_grid(grid, print_decoration=True, w=1):
    x_values = [x for x, _ in grid.keys()]
    y_values = [y for _, y in grid.keys()]
    min_x = min(x_values)
    min_y = min(y_values)
    max_x = max(x_values) + 1
    max_y = max(y_values) + 1
    if print_decoration:
        print('grid:', min_x, max_x, min_y, max_y)
    for y in range(min_y, max_y):
        row = []
        for x in range(min_x, max_x):
            entry = grid.get((x, y))
            if entry is not None:
                row.append(entry * w)
            else:
                row.append(' ' * w)
        print(''.join(row))
    if print_decoration:
        print('========')


# Determine all shortest distances within the grid from start position
# until either target position is reached or all reachable grid elements
# are processed. Grid elements which are walls ('#' by default) are not
# considered as being reachable.
# The result is a path grid (dict) which contains for every position from
# the original grid (or just until the target position was processed) the
# shortest distance to the start_pos and the x and y coordinate of each
# predecessor within the grid.
def determine_grid_path(start_pos, direction, grid, target=None, wall='#'):
    grid_path = {}

    cost = {0: 1, 1: 1001, 3: 1001}

    cx, cy = start_pos
    visited = set()
    to_visit = []
    heapq.heappush(to_visit, (0, cx, cy, direction, cx, cy))
    while len(to_visit) > 0:
        dist, cx, cy, di, px, py = heapq.heappop(to_visit)
        pos = (cx, cy, di)
        if pos in visited:
            continue
        visited.add(pos)
        grid_path[(cx, cy)] = (dist, px, py)
        if target and (cx, cy) == target:
            break
        for d_diff in [0, 1, 3]:
            ndi = (di + d_diff) % 4
            n_dist = dist + cost[d_diff]
            dx, dy = dxy[ndi]
            nx, ny = cx + dx, cy + dy
            next_grid_entry = grid.get((nx, ny))
            if next_grid_entry is not None and next_grid_entry != wall and (nx, ny, ndi) not in visited:
                heapq.heappush(to_visit, (n_dist, nx, ny, ndi, cx, cy))
    return grid_path


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    sx, sy = 0, 0
    tx, ty = 0, 0
    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == 'S':
                sx, sy = x, y
            if ch == 'E':
                tx, ty = x, y
            grid[(x, y)] = ch

    path = determine_grid_path((sx, sy), 1, grid, (tx, ty))
    p1 = path[(tx, ty)][0]

    current_path = set()
    current_path.add((sx, sy))
    paths = determine_grid_paths(sx, sy, 1, grid, tx, ty, p1)

    ans = set()
    ans.add((sx, sy))
    for path in paths:
        cost, p = path
        if cost == p1:
            ans.update(p)
    p2 = len(ans)

    return p1, p2


def determine_grid_paths(sx, sy, start_direction, grid, tx, ty, min_costs):
    cost = {0: 1, 1: 1001, 3: 1001}

    ans = []
    best_distances = {}

    q = deque()
    q.append((sx, sy, start_direction, set(), 0, set()))
    while q:
        (cx, cy, direction, current_path, current_cost, visited) = q.popleft()
        if cx == tx and cy == ty:
            ans.append((current_cost, current_path))
            continue

        if (cx, cy, direction) in best_distances:
            bd = best_distances[(cx, cy, direction)]
            if bd > current_cost:
                best_distances[(cx, cy, direction)] = current_cost
            elif current_cost > bd:
                continue
        else:
            best_distances[(cx, cy, direction)] = current_cost

        pos = (cx, cy, direction)
        if pos in visited:
            continue
        visited.add(pos)

        for d_diff in [0, 1, 3]:
            new_direction = (direction + d_diff) % 4
            new_cost = current_cost + cost[d_diff]
            if new_cost > min_costs:
                continue

            dx, dy = dxy[new_direction]
            nx, ny = cx + dx, cy + dy
            next_grid_entry = grid.get((nx, ny))
            if next_grid_entry is not None and next_grid_entry != '#' and (nx, ny, new_direction) not in visited:
                new_visited = set(visited)
                new_current_path = set(current_path)
                new_current_path.add((nx, ny))
                q.append((nx, ny, new_direction, new_current_path, new_cost, new_visited))
    return ans


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
