import time
from collections import *
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


def read_grid(raw_grid):
    robot = None
    grid = {}
    for y, line in enumerate(raw_grid):
        for x, ch in enumerate(line):
            if ch == '@':
                robot = (x, y)
                ch = '.'
            grid[(x, y)] = ch
    # print(robot)
    # print_grid(grid)
    return grid, robot


def read_big_grid(raw_grid):
    robot = None
    grid = {}
    for y, line in enumerate(raw_grid):
        for x, ch in enumerate(line):
            if ch == '@':
                robot = (2 * x, y)
                ch = '.'
            ch1 = ch2 = ch
            if ch == 'O':
                ch1, ch2 = '[', ']'
            grid[(2 * x, y)] = ch1
            grid[(2 * x + 1, y)] = ch2
    # print(robot)
    # print_grid(grid)
    return grid, robot


def solve_puzzle(filename, param=None, verbose=False):
    groups = [[line.strip() for line in group.split('\n')] for group in open(filename, 'r').read().split('\n\n')]
    raw_grid, moves = groups

    grid, robot = read_grid(raw_grid)
    move_robot(grid, robot, moves)
    p1 = calc_gps_score(grid)
    # print_grid(grid)

    grid, robot = read_big_grid(raw_grid)
    move_robot(grid, robot, moves)
    p2 = calc_gps_score(grid)
    # print_grid(grid)

    return p1, p2


def move_robot(grid, robot, moves):
    d_mov = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
    rx, ry = robot
    for line in moves:
        for mov in line:
            dx, dy = d_mov[mov]
            nx, ny = rx + dx, ry + dy
            nch = grid[(nx, ny)]
            if nch == '#':
                pass
            elif nch == '.':
                rx, ry = nx, ny
            elif nch in '[]O':
                q = deque()
                q.append((rx, ry))
                to_move = set()
                can_move = True
                while q:
                    cx, cy = q.popleft()
                    if (cx, cy) in to_move:
                        continue
                    to_move.add((cx, cy))
                    ncx, ncy = cx + dx, cy + dy
                    nch = grid[(ncx, ncy)]
                    if nch == '#':
                        can_move = False
                        break
                    elif nch == '[':
                        assert grid[(ncx + 1, ncy)] == ']'
                        q.append((ncx, ncy))
                        q.append((ncx + 1, ncy))
                    elif nch == ']':
                        assert grid[(ncx - 1, ncy)] == '['
                        q.append((ncx, ncy))
                        q.append((ncx - 1, ncy))
                    elif nch == 'O':
                        q.append((ncx, ncy))
                    else:
                        assert nch == '.'
                if can_move:
                    while to_move:
                        for mx, my in to_move:
                            nmx, nmy = mx + dx, my + dy
                            if (nmx, nmy) in to_move:
                                continue
                            assert grid[(nmx, nmy)] == '.'
                            grid[(nmx, nmy)] = grid[(mx, my)]
                            grid[(mx, my)] = '.'
                            break
                        to_move.remove((mx, my))
                    rx, ry = nx, ny
            else:
                assert False


def calc_gps_score(grid):
    gps_score = 0
    for (x, y), ch in grid.items():
        if ch in '[O':
            gps_score += 100 * y + x
    return gps_score


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
