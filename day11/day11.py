import re
import time
from collections import *
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


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


def solve_puzzle_1(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    inp = nums(lines[0])
    for loop in range(25):
        idx = 0
        while idx < len(inp):
            stone = inp[idx]
            if stone == 0:
                inp[idx] = 1
                idx += 1
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                half_len = len(str_stone) // 2
                left = int(str_stone[:half_len])
                right = int(str_stone[half_len:])
                inp[idx] = left
                inp.insert(idx + 1, right)
                idx += 2
            else:
                inp[idx] *= 2024
                idx += 1

    p1 = len(inp)
    p2 = 0

    return p1, p2


def solve_puzzle_2(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    inp = nums(lines[0])

    root = None
    prev = None
    for stone in inp:
        nxt = Node(stone)
        if root is None:
            root = nxt
        if prev is not None:
            prev.insert_after(nxt)
        prev = nxt

    for loop in range(25):
        nxt = root
        while nxt is not None:
            stone = nxt.value
            if stone == 0:
                nxt.value = 1
                nxt = nxt.nxt
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                half_len = len(str_stone) // 2
                left = int(str_stone[:half_len])
                right = int(str_stone[half_len:])
                nxt.value = left
                new_node = Node(right)
                nxt.insert_after(new_node)
                nxt = new_node.nxt
            else:
                nxt.value *= 2024
                nxt = nxt.nxt

    p1, p2 = 0, 0
    nxt = root
    while nxt is not None:
        p1 += 1
        nxt = nxt.nxt

    return p1, p2


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    inp = nums(lines[0])

    stones = defaultdict(int)
    for stone in inp:
        stones[stone] += 1

    for loop in range(75):
        if loop == 25:
            p1 = count_stones(stones)

        new_stones = defaultdict(int)
        for stone, n in stones.items():
            if stone == 0:
                new_stones[1] += n
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                half_len = len(str_stone) // 2
                left = int(str_stone[:half_len])
                right = int(str_stone[half_len:])
                new_stones[left] += n
                new_stones[right] += n
            else:
                new_stones[stone * 2024] += n
        stones = new_stones

    p2 = count_stones(stones)

    return p1, p2


def count_stones(stones):
    ans = 0
    for stone, n in stones.items():
        ans += n
    return ans


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, None],
        ['data.txt',    'real data    ', True,  False, None],
    ]

    for filename, description, use_data, verbose, param in input_data_list:
        if use_data:
            start = time.time()
            # p1, p2 = solve_puzzle_1('data/' + filename, param, verbose)
            # p1, p2 = solve_puzzle_2('data/' + filename, param, verbose)
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
