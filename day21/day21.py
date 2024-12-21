import time
import itertools
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

'''
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
'''
robo_pad = {             '^': (1, 0), 'A': (2, 0),
            '<': (0, 1), 'v': (1, 1), '>': (2, 1)}


def solve_puzzle_1(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    codes = []
    p1, p2 = 0, 0

    inp = []
    for y, line in enumerate(lines):
        inp.append(line)

    mx, my = (2, 3)
    r1x, r1y = (2, 0)
    r2x, r2y = (2, 0)
    for code in inp:
        possibilities, mx, my = move_pad(num_pad, code, mx, my)

        min_len = min([len(possi) for possi in possibilities])
        second_possibilities = []
        for possi in possibilities:
            if len(possi) > min_len:
                continue
            add_2nd_possiblities, r1x, r1y = move_pad(robo_pad, possi, r1x, r1y)
            second_possibilities.extend(add_2nd_possiblities)

        min_len = min([len(possi2) for possi2 in second_possibilities])
        third_possibilities = []
        for possi2 in second_possibilities:
            if len(possi2) > min_len:
                continue
            add_3nd_possiblities, r2x, r2y = move_pad(robo_pad, possi2, r2x, r2y)
            third_possibilities.extend(add_3nd_possiblities)

        best_code = third_possibilities[0]
        for new_code in third_possibilities[1:]:
            if len(new_code) < len(best_code):
                best_code = new_code
        codes.append(best_code)

    for idx, code in enumerate(codes):
        inpt = int(inp[idx][:-1])
        ans = len(code) * inpt
        print(len(code), inpt, ans, inp[idx], inp[idx][:-1], ''.join(code))
        p1 += ans

    return p1, p2


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    inp = []
    for y, line in enumerate(lines):
        inp.append(line)

    optimal_moves_num_pad = calc_optimal_moves(num_pad)
    optimal_moves_robo_pad = calc_optimal_moves(robo_pad)
    optimal_length_moves_robo_pad = {k: len(v[0]) for k, v in optimal_moves_robo_pad.items()}
    cache = {}

    def calc_length(code, loop):
        if (code, loop) in cache:
            return cache[(code, loop)]

        min_length = 0
        if loop == 1:
            prev_digit = 'A'
            for digit in code:
                min_length += optimal_length_moves_robo_pad[(prev_digit, digit)]
                prev_digit = digit
        else:
            prev_digit = 'A'
            for digit in code:
                length_list = []
                if (prev_digit, digit) not in optimal_moves_robo_pad:
                    print(code, loop, prev_digit, digit)
                for next_code in optimal_moves_robo_pad[(prev_digit, digit)]:
                    length_list.append(calc_length(next_code, loop - 1))
                prev_digit = digit
                min_length += min(length_list)

        cache[(code, loop)] = min_length
        return min_length

    def calc_min_length(num_pad_moves, loop):
        length_list = []
        for move in num_pad_moves:
            length_list.append(calc_length(move, loop))
        min_len = min(length_list)
        return min_len

    for code in inp:
        num = int(code[:-1])
        num_pad_moves = calc_moves(code, optimal_moves_num_pad)
        min_len_p1 = calc_min_length(num_pad_moves, 2)
        p1 += min_len_p1 * num
        min_len_p2 = calc_min_length(num_pad_moves, 25)
        p2 += min_len_p2 * num
        # print(code, num, min_len_p1, min_len_p2)

    return p1, p2


def calc_moves(code, optimal_moves_pad):
    moves = []
    prev_digit = 'A'
    for digit in code:
        moves.append(optimal_moves_pad[(prev_digit, digit)])
        prev_digit = digit
    moves = itertools.product(*moves)
    moves = [''.join(move) for move in moves]
    return moves


def calc_optimal_moves(pad):
    optimal_moves = {}
    for d1, p1 in pad.items():
        for d2, p2 in pad.items():
            if d1 == d2:
                optimal_moves[(d1, d2)] = ['A']
            else:
                cx, cy = p1
                tx, ty = p2
                dx, dy = tx - cx, ty - cy
                possibilities = move_pad_once(pad, cx, cy, dx, dy, [[]])
                min_len = min([len(possibility) for possibility in possibilities])
                filtered_possibilities = [''.join(possibility) for possibility in possibilities if len(possibility) == min_len]
                if len(filtered_possibilities) < len(possibilities):
                    print(d1, d2, len(possibilities), len(filtered_possibilities))
                optimal_moves[(d1, d2)] = filtered_possibilities
    return optimal_moves


def move_pad(pad, code, cx, cy):
    possibilities = [[]]
    for digit in code:
        tx, ty = pad[digit]
        dx, dy = tx - cx, ty - cy
        extended_possibilities = move_pad_once(pad, cx, cy, dx, dy, possibilities)
        cx, cy = tx, ty
        min_len = min([len(ext_possi) for ext_possi in extended_possibilities])
        possibilities = [ext_possi for ext_possi in extended_possibilities if len(ext_possi) == min_len]
    return possibilities, cx, cy


def move_pad_once(pad, cx, cy, dx, dy, possibilities):
    if dx == 0 and dy == 0:
        for possi in possibilities:
            possi.append('A')
        return possibilities

    new_possibilities = []
    if dx > 0:
        nx, ny = cx + 1, cy
        if (nx, ny) in pad.values():
            step_new_possis = []
            for possi in possibilities:
                new_possi = list(possi)
                new_possi.append('>')
                step_new_possis.append(new_possi)
            new_possibilities.extend(move_pad_once(pad, nx, ny, dx - 1, dy, step_new_possis))
    if dx < 0:
        nx, ny = cx - 1, cy
        if (nx, ny) in pad.values():
            step_new_possis = []
            for possi in possibilities:
                new_possi = list(possi)
                new_possi.append('<')
                step_new_possis.append(new_possi)
            new_possibilities.extend(move_pad_once(pad, nx, ny, dx + 1, dy, step_new_possis))
    if dy > 0:
        nx, ny = cx, cy + 1
        if (nx, ny) in pad.values():
            step_new_possis = []
            for possi in possibilities:
                new_possi = list(possi)
                new_possi.append('v')
                step_new_possis.append(new_possi)
            new_possibilities.extend(move_pad_once(pad, nx, ny, dx, dy - 1, step_new_possis))
    if dy < 0:
        nx, ny = cx, cy - 1
        if (nx, ny) in pad.values():
            step_new_possis = []
            for possi in possibilities:
                new_possi = list(possi)
                new_possi.append('^')
                step_new_possis.append(new_possi)
            new_possibilities.extend(move_pad_once(pad, nx, ny, dx, dy + 1, step_new_possis))
    return new_possibilities


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
