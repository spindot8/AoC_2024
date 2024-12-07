import time


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


def find_horizontal(inp, h, w, to_find_word):
    to_find_list = [to_find_word, to_find_word[::-1]]

    ans = 0
    for y in range(h):
        for x in range(w):
            for to_find in to_find_list:
                if inp[y][x:].startswith(to_find):
                    ans += 1
    return ans


def find_vertical(inp, h, w, to_find_word):
    wl = len(to_find_word)
    to_find_list = [to_find_word, to_find_word[::-1]]

    ans = 0
    for x in range(w):
        for y in range(h - wl + 1):
            for to_find in to_find_list:
                match = True
                for i, ch in enumerate(to_find):
                    if inp[y + i][x] != ch:
                        match = False
                        break
                if match:
                    ans += 1
    return ans


def find_diagonal(inp, h, w, to_find_word):
    wl = len(to_find_word)
    to_find_list = [to_find_word, to_find_word[::-1]]

    ans = 0
    for y in range(h - wl + 1):
        for x in range(w - wl + 1):
            for to_find in to_find_list:
                match = True
                for i, ch in enumerate(to_find):
                    if inp[y + i][x + i] != ch:
                        match = False
                        break
                if match:
                    ans += 1

                match = True
                for i, ch in enumerate(to_find):
                    if inp[y + wl - i - 1][x + i] != ch:
                        match = False
                        break
                if match:
                    ans += 1
    return ans


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1 = 0
    p2 = 0

    h = len(lines)
    w = len(lines[0])
    inp = lines

    to_find = 'XMAS'
    p1 += find_horizontal(inp, h, w, to_find)
    p1 += find_vertical(inp, h, w, to_find)
    p1 += find_diagonal(inp, h, w, to_find)

    to_find = 'MAS'
    to_find_r = 'SAM'
    wl = len(to_find)

    for y in range(h - wl + 1):
        for x in range(w - wl + 1):
            match_v = True
            for i, ch in enumerate(to_find):
                if inp[y+i][x+i] != ch:
                    match_v = False
                    break

            match_b = True
            for i, ch in enumerate(to_find_r):
                if inp[y+i][x+i] != ch:
                    match_b = False
                    break

            match_v2 = True
            for i, ch in enumerate(to_find_r):
                if inp[y + wl - i - 1][x+i] != ch:
                    match_v2 = False
                    break

            match_b2 = True
            for i, ch in enumerate(to_find):
                if inp[y + wl - i - 1][x+i] != ch:
                    match_b2 = False
                    break

            if match_v and (match_v2 or match_b2):
                p2 += 1

            if match_b and (match_b2 or match_v2):
                p2 += 1

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
