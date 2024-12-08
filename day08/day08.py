import time
from collections import *
from copy import deepcopy
import pyperclip


def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    antennas = defaultdict(list)
    grid_p1 = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            grid_p1[(x, y)] = ch
            if ch != '.':
                antennas[ch].append([x, y])

    grid_p2 = deepcopy(grid_p1)
    anti_nodes_p1 = set()
    anti_nodes_p2 = set()
    for _, v in antennas.items():
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                x1, y1 = v[i]
                x2, y2 = v[j]
                determine_anti_nodes(grid_p1, anti_nodes_p1, x1, y1, x2, y2, True)
                determine_anti_nodes(grid_p2, anti_nodes_p2, x1, y1, x2, y2, False)

    p1 = len(anti_nodes_p1)
    p2 = len(anti_nodes_p2)

    return p1, p2


def determine_anti_nodes(grid, anti_nodes, x1, y1, x2, y2, part1):
    dx, dy = x2 - x1, y2 - y1
    ax1, ay1 = x1, y1
    ax2, ay2 = x2, y2

    while True:
        ax1, ay1 = ax1 - dx, ay1 - dy
        if (ax1, ay1) in grid:
            anti_nodes.add((ax1, ay1))
            grid[(ax1, ay1)] = '#'
        else:
            break
        if part1:
            break

    while True:
        ax2, ay2 = ax2 + dx, ay2 + dy
        if (ax2, ay2) in grid:
            anti_nodes.add((ax2, ay2))
            grid[(ax2, ay2)] = '#'
        else:
            break
        if part1:
            break

    if not part1:
        anti_nodes.add((x1, y1))
        anti_nodes.add((x2, y2))


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
