import sys
import math
import hashlib
import re
import time
import itertools
from collections import *
from random import shuffle
from copy import deepcopy
# import networkx as netx
# import sympy
import heapq
import functools
from functools import cmp_to_key


# How to sort a list with an own compare function my_compare_function.
# The compare function must take two arguments left and right and return back:
# -1 when left is less than right
# 0 when left is equal to right
# +1 when left is bigger than right
# [].sort(key=cmp_to_key(my_compare_function))

# format as binary with in this case at least 8 digits
# print("{:08b}".format(13))

# Shoelace algorithm: https://www.101computing.net/the-shoelace-algorithm/
# Gaußsche Trapezformel: https://de.wikipedia.org/wiki/Gau%C3%9Fsche_Trapezformel
# Ordered corners of the polygon: [(x1, y1), (x2, y2), (x3, y3), ..., (xn-1, yn-1), (xn, yn)]
# area = abs(x1*y2 - x2*y1 + x2*y3 - x3*y2 + ... + xn-1*yn - xn*yn-1 + xn*y1 - x1*yn) // 2

# Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
# Satz von Pick: https://de.wikipedia.org/wiki/Satz_von_Pick
# A = area of the polygon calculated with Shoelace algorithm
# I = inner area without border = dots within the polygon
# R = border length = dots on the border of the polygon
# A = I + R//2 - 1
# I = A - R//2 + 1
# AREA_WITH_BORDER = I + R = A - R//2 + 1 + R = A + R // 2 + 1


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
di = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
# di = {'N': 0, 'E': 1, 'S': 2, 'W': 3}

UP = NORTH = 0
RIGHT = EAST = 1
DOWN = SOUTH = 2
LEFT = WEST = 3


#        NORTH -> CLOCKWISE with diagonals
ddxy = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
# 3D dxyz
dxyz = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha_lower_upper = alpha_lower + alpha_upper


# Paint the supplied - horizontal or vertical - lines into the supplied grid.
# The supplied lines list should have the format [(x1, y1), (x2, y2), (x3, y3), ..., (xn, yn)].
# The line is drawn between x1, y1 and x2, y2. The next line between x2, y2 and x3, y3 and so on.
# In order to have only horizontal and vertical lines, either xn and xn+1 must be equal (vertical line)
# or yn and yn+1 must be equal (horizontal line).
def paint_lines_into_grid(grid: dict, lines: list, line_ch='#'):
    assert len(lines) >= 2

    (x1, y1) = lines[0]
    for (x2, y2) in lines[1:]:
        assert x1 == x2 or y1 == y2

        dx, dy = x2 - x1, y2 - y1
        sx, sy = sign(dx), sign(dy)
        steps = max(abs(dx), abs(dy)) + 1
        for m in range(steps):
            nx = x1 + (m * sx)
            ny = y1 + (m * sy)
            grid[(nx, ny)] = line_ch
        x1, y1 = x2, y2


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


# Merge the supplied ranges as far as possible.
# The supplied ranges must be a list of tuples, e. g. like:
# [(xl1, xh1), (xl2, xh2), (xl3, xh3), (xl3, xh3), ...]
# [(5, 8), (64, 128), (1, 3), (2, 9), (-3, 20), (13, 31)]
# It must be tuples in order to sort them (compare them).
# They must not be sorted when supplied to the function.
# A merged and sorted list will be returned which looks like this:
# [[mxl1, mxh1], [mxl2, mxh2]]
# [[-3, 31], [64, 128]]
def merge_ranges(ranges):
    merged_ranges = []
    ranges.sort()
    for xl, xh in ranges:
        if len(merged_ranges) == 0:
            merged_ranges.append([xl, xh])
            continue

        qxl, qxh = merged_ranges[-1]
        if xl > qxh + 1:
            merged_ranges.append([xl, xh])
        else:
            merged_ranges[-1][1] = max(xh, qxh)
    return merged_ranges


# Return the sign of the supplied number, -1 if the number is negative,
# 1 if the number is positive or 0 if the number is zero.
def sign(num):
    return 1 if num > 0 else -1 if num < 0 else 0


# Calculates the least common multiply of two integer number.
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


# Calculates the least common multiply of all integer numbers contained in lst.
def lcm_prod(lst):
    ans = 1
    for e in lst:
        ans = lcm(ans, e)
    return ans


# Calculates the number which fulfills the supplied conditions by using the
# chinese remainder theorem. The supplied conditions must be in this format:
# [[remainder 1, divisor 1], [remainder 2, divisor 2], [remainder 3, divisor 3], ..., [remainder n, divisor n]]
# These conditions mean that the answer number which is searched must have the
# according remainder x when divided through the divisor x for supplied pairs of
# remainders and divisors. All the supplied divisors must not have a common divider.
def chinese_remainder(conditions):
    ans = 0
    full_product = math.prod(d for _, d in conditions)

    assert full_product == lcm_prod([d for _, d in conditions])
    assert all([r < d for r, d in conditions])

    for remainder, divisor in conditions:
        factor = 1
        product = full_product // divisor
        while (factor * product) % divisor != remainder:
            factor += 1
        ans += factor * product

    ans %= full_product
    return ans


# Transpose the grid that rows get columns and columns get rows.
#          16A
# 12345    27B
# 67890 -> 38C
# ABCDE    49D
#          50E
def transpose_rows_to_columns(grid):
    return list(map(list, zip(*grid)))


# Rotate the grid 90 degree clockwise.
#          A61
# 12345    B72
# 67890 -> C83
# ABCDE    D94
#          E05
def rotate_90_degree_clockwise(grid):
    return [row[::-1] for row in transpose_rows_to_columns(grid)]


# Rotate the grid 90 degree counterclockwise.
#          50E
# 12345    49D
# 67890 -> 38C
# ABCDE    27B
#          16A
def rotate_90_degree_counterclockwise(grid):
    return transpose_rows_to_columns(grid)[::-1]


# Rotate the grid 180 degree.
# 12345    EDCBA
# 67890 -> 09876
# ABCDE    54321
def rotate_180_degree(grid):
    return [row[::-1] for row in grid][::-1]


# Flip the grid vertical.
# 12345    ABCDE
# 67890 -> 67890
# ABCDE    12345
def flip_vertical(grid):
    return [row for row in grid][::-1]


# Flip the grid horizontal.
# 12345    54321
# 67890 -> 09876
# ABCDE    EDCBA
def flip_horizontal(grid):
    return [row[::-1] for row in grid]


class Node:
    def __init__(self, value, nxt=None, prev=None):
        self.value = value
        self.nxt = nxt
        self.prev = prev

    def insert_after(self, node):
        old_nxt = self.nxt
        self.nxt = node
        node.prev = self
        node.nxt = old_nxt
        if old_nxt is not None:
            old_nxt.prev = node

    def insert_before(self, node):
        old_prev = self.prev
        self.prev = node
        node.prev = old_prev
        node.nxt = self
        if old_prev is not None:
            old_prev.nxt = node

    def unlink_node(self):
        prev_node = self.prev
        next_node = self.nxt
        if prev_node is not None:
            prev_node.nxt = next_node
        if next_node is not None:
            next_node.prev = prev_node
        return prev_node, next_node


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def s_nums(line):
    return [int(x) for x in re.findall(r'-?[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]
    # groups = [[line.strip() for line in group.split('\n')] for group in open(filename, 'r').read().split('\n\n')]

    p1, p2 = 0, 0

    # inp = [int(x) for x in lines[0]]
    # inp = [int(x) for x in lines[0].split(',')]
    # inp = [(x, y) for y, line in enumerate(lines) for x, ch in enumerate(line) if ch == '#']

    # grid = {}
    # for y, line in enumerate(lines):
    #     for x, ch in enumerate(line):
    #         grid[(x, y)] = ch

    # h = len(lines)
    # w = len(lines[0])

    inp = []
    # for lines in groups:
    for y, line in enumerate(lines):
        # for x, ch in enumerate(line):
        # inp.append(line)
        inp.append(nums(line))
        # inp.append(s_nums(line))
        # inp.append(int(line))
        # inp.append(line.split())
        # inp.append([x for x in line])
        # inp.append([int(x) for x in line])
        # inp.append([int(x) for x in line.split(',')])
        # inp.append([list(map(int, p.split(','))) for p in line.split(' -> ')])
        # inp.append([int(x) for x in re.findall('[0-9]+', line)])
        # inp.append([int(x) for x in re.findall('-?[0-9]+', line)])

    for e in inp:
        print(e)

    return p1, p2


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
            print(p1)
            print(p2)
            print("%s \tin %d ms" % (description, round(1000 * (end - start), 2)))


if __name__ == '__main__':
    main()
