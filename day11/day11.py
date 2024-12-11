import re
import time
from collections import *
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    stones = Counter(nums(lines[0]))
    for loop in range(75):
        if loop == 25:
            p1 = count_stones(stones)

        new_stones = defaultdict(int)
        for stone, n in stones.items():
            if stone == 0:
                new_stones[1] += n
            elif len(str(stone)) % 2 == 0:
                left, right = cut_stone(stone)
                new_stones[left] += n
                new_stones[right] += n
            else:
                new_stones[stone * 2024] += n
        stones = new_stones

    p2 = count_stones(stones)

    return p1, p2


def cut_stone(stone):
    str_stone = str(stone)
    half_len = len(str_stone) // 2
    left = int(str_stone[:half_len])
    right = int(str_stone[half_len:])
    return left, right


def count_stones(stones):
    return sum([n for n in stones.values()])


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
