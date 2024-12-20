import time
from collections import *
import pyperclip


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def determine_simple_path(sx, sy, simple_grid: set):
    grid_path = {}
    visited = set()
    q = deque([(0, sx, sy)])
    while q:
        dist, cx, cy = q.popleft()
        pos = (cx, cy)
        if pos not in visited:
            visited.add(pos)
            grid_path[pos] = dist
            for dx, dy in dxy:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in simple_grid and (nx, ny) not in visited:
                    q.append((dist + 1, nx, ny))
    return grid_path


def determine_cheating_ends(simple_grid, pos, cheat_time):
    cheating_ends = set()
    for dist in range(1, cheat_time + 1):
        for dx in range(dist + 1):
            dy = dist - dx
            for mx, my in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = pos[0] + (dx * mx), pos[1] + (dy * my)
                if (nx, ny) in simple_grid:
                    cheating_ends.add((nx, ny))
    return cheating_ends


def determine_cheats(simple_grid: set, cheat_time, normal_target_distance, distance_threshold, distances):
    ans = 0
    for start_pos in simple_grid:
        cheating_ends = determine_cheating_ends(simple_grid, start_pos, cheat_time)
        for end_pos in cheating_ends:
            cheating_distance = abs(end_pos[0] - start_pos[0]) + abs(end_pos[1] - start_pos[1])
            assert cheating_distance <= cheat_time
            dist = distances[start_pos] + cheating_distance + (normal_target_distance - distances[end_pos])
            if dist <= normal_target_distance - distance_threshold:
                ans += 1
    return ans


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    simple_grid = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == 'S':
                sx, sy = x, y
            if ch == 'E':
                tx, ty = x, y
            if ch != '#':
                simple_grid.add((x, y))

    distances = determine_simple_path(sx, sy, simple_grid)
    normal_target_distance = distances[(tx, ty)]

    threshold_p1, threshold_p2 = param
    p1 = determine_cheats(simple_grid, 2, normal_target_distance, threshold_p1, distances)
    p2 = determine_cheats(simple_grid, 20, normal_target_distance, threshold_p2, distances)

    return p1, p2


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, (1, 50)],
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
