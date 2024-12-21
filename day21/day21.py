import time
import itertools
from collections import *
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


'''
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
'''
num_pad = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
           '4': (0, 1), '5': (1, 1), '6': (2, 1),
           '1': (0, 2), '2': (1, 2), '3': (2, 2),
                        '0': (1, 3), 'A': (2, 3)}
rev_num_pad = {v: k for k, v in num_pad.items()}

'''
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
'''
robo_pad = {             '^': (1, 0), 'A': (2, 0),
            '<': (0, 1), 'v': (1, 1), '>': (2, 1)}
rev_robo_pad = {v: k for k, v in robo_pad.items()}


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    codes = []
    for y, line in enumerate(lines):
        codes.append(line)

    moves_num_pad = calc_pad_moves(rev_num_pad)
    moves_robo_pad = calc_pad_moves(rev_robo_pad)
    length_moves_robo_pad = {k: len(v[0]) for k, v in moves_robo_pad.items()}
    cache = {}

    def calc_length(code, loop):
        if (code, loop) in cache:
            return cache[(code, loop)]

        min_length = 0
        if loop == 1:
            prev_digit = 'A'
            for digit in code:
                min_length += length_moves_robo_pad[(prev_digit, digit)]
                prev_digit = digit
        else:
            prev_digit = 'A'
            for digit in code:
                next_min_len = int(1e12)
                for next_code in moves_robo_pad[(prev_digit, digit)]:
                    next_min_len = min(next_min_len, calc_length(next_code, loop - 1))
                prev_digit = digit
                min_length += next_min_len

        cache[(code, loop)] = min_length
        return min_length

    p1, p2 = 0, 0
    for code in codes:
        num = int(code[:-1])
        num_pad_moves = calc_num_pad_moves(code, moves_num_pad)

        min_len_p1 = min(calc_length(move, 2) for move in num_pad_moves)
        p1 += min_len_p1 * num

        min_len_p2 = min(calc_length(move, 25) for move in num_pad_moves)
        p2 += min_len_p2 * num

    return p1, p2


def calc_num_pad_moves(code: str, moves_num_pad: dict):
    moves = []
    prev_digit = 'A'
    for digit in code:
        moves.append(moves_num_pad[(prev_digit, digit)])
        prev_digit = digit
    moves = [''.join(move) for move in itertools.product(*moves)]
    return moves


def calc_pad_moves(rev_pad: dict):
    optimal_moves = {}
    for p1, d1 in rev_pad.items():
        for p2, d2 in rev_pad.items():
            if d1 == d2:
                optimal_moves[(d1, d2)] = ['A']
            else:
                possibilities = possible_pad_moves_between_two_keys(rev_pad, p1, p2)
                optimal_moves[(d1, d2)] = possibilities
    return optimal_moves


def possible_pad_moves_between_two_keys(rev_pad: dict, start_pos, target_pos):
    possibilities = []

    min_length = int(1e6)
    sx, sy = start_pos
    q = deque([(sx, sy, '')])
    while q:
        cx, cy, path = q.popleft()
        for dx, dy, dm in [(0, -1, '^'), (1, 0, '>'), (0, 1, 'v'), (-1, 0, '<')]:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) in rev_pad:
                new_path = path + dm
                if (nx, ny) == target_pos:
                    min_length = min(min_length, len(new_path))
                    if len(new_path) <= min_length:
                        possibilities.append(new_path + 'A')
                    else:
                        break
                else:
                    if len(new_path) < min_length:
                        q.append((nx, ny, new_path))
    return possibilities


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
