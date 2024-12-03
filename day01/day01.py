import time
from collections import *


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    left = []
    right = []
    for y, line in enumerate(lines):
        ln, rn = [int(x) for x in line.split()]
        left.append(ln)
        right.append(rn)

    cnt_right = Counter(right)

    left.sort()
    right.sort()
    for ln, rn in zip(left, right):
        p1 += abs(ln - rn)
        p2 += ln * cnt_right.get(ln, 0)

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
