import math
import re
import time
import pyperclip


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


def s_nums(line):
    return [int(x) for x in re.findall(r'-?[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0
    w, h, diagonal_count = param

    robots = []
    for y, line in enumerate(lines):
        robots.append(s_nums(line))

    loop = 0
    while p1 == 0 or p2 == 0:
        loop += 1

        grid = {}
        for idx in range(len(robots)):
            cx, cy, vx, vy = robots[idx]
            nx, ny, = cx + vx, cy + vy
            if nx < 0:
                nx += w
            elif nx >= w:
                nx -= w
            if ny < 0:
                ny += h
            elif ny >= h:
                ny -= h
            robots[idx][0] = nx
            robots[idx][1] = ny
            grid[(nx, ny)] = '#'

        if loop == 100:
            p1 = determine_safety_factor(robots, h, w)

        for (x, y) in grid:
            diagonal = True
            for i in range(1, diagonal_count):
                nx, ny = x + i, y - i
                if (nx, ny) not in grid:
                    diagonal = False
                    break

            if diagonal:
                # print_grid(grid)
                p2 = loop
                break

    return p1, p2


def determine_safety_factor(robots, h, w):
    qh = h // 2
    qw = w // 2

    cnt = [0, 0, 0, 0]
    for idx, (cx, cy, _, _) in enumerate(robots):
        if 0 <= cx < qw and 0 <= cy < qh:
            cnt[0] += 1
        if qw + 1 <= cx < w and 0 <= cy < qh:
            cnt[1] += 1
        if 0 <= cx < qw and qh + 1 <= cy < h:
            cnt[2] += 1
        if qw + 1 <= cx < w and qh + 1 <= cy < h:
            cnt[3] += 1
    return math.prod(cnt)


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, (11, 7, 1)],
        ['data.txt',    'real data    ', True,  False, (101, 103, 10)],
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
