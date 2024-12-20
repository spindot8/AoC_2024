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


def determine_cheats(start_pos, grid, normal_dist, dist_threshold, max_cheat_time, normal_distances, wall='#'):
    ans = set()

    sx, sy = start_pos
    visited = set()
    to_visit = deque()
    to_visit.append((0, sx, sy, None, None))
    while len(to_visit) > 0:
        dist, cx, cy, cheat_start_pos, cheat_time = to_visit.popleft()

        if dist > normal_dist - dist_threshold:
            continue

        key = (cx, cy, cheat_start_pos, cheat_time)
        if key in visited:
            continue
        visited.add(key)

        # start cheating whenever possible
        if cheat_start_pos is None:
            to_visit.append((dist, cx, cy, (cx, cy), max_cheat_time))
        else:
            # end cheating whenever possible (not in a wall), it can be shorter than max_cheat_time
            if grid[(cx, cy)] != wall:
                assert cheat_time is not None and cheat_time >= 0
                current_normal_dist = normal_distances[(cx, cy)]
                if dist <= current_normal_dist - dist_threshold:
                    ans.add((cheat_start_pos, (cx, cy)))
                    # print(dist, cheat_start_pos, (cx, cy), len(ans))

        for dx, dy in dxy:
            nx, ny = cx + dx, cy + dy
            next_grid_entry = grid.get((nx, ny))

            if next_grid_entry is not None:
                if cheat_start_pos is not None and cheat_time is not None:
                    if cheat_time > 0:
                        to_visit.append((dist + 1, nx, ny, cheat_start_pos, cheat_time - 1))
                else:
                    if next_grid_entry != wall:
                        to_visit.append((dist + 1, nx, ny, cheat_start_pos, cheat_time))

    return len(ans)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == 'S':
                sx, sy = x, y
            if ch == 'E':
                tx, ty = x, y
            grid[(x, y)] = ch

    path = determine_grid_path((sx, sy), grid)
    normal_distances = {}
    for pos, (dist, px, py) in path.items():
        normal_distances[pos] = dist
    normal_distance = normal_distances[(tx, ty)]

    threshold_p1, threshold_p2 = param
    p1 = determine_cheats((sx, sy), grid, normal_distance, threshold_p1, 2, normal_distances)
    p2 = determine_cheats((sx, sy), grid, normal_distance, threshold_p2, 20, normal_distances)

    return p1, p2


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, (1, 50)],
        # takes about 50 seconds
        ['data.txt',    'real data    ', True,  False, (100, 100)],
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
