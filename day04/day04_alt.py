import time


#        NORTH -> CLOCKWISE with diagonals
ddxy = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def solve_puzzle(filename, param=None, verbose=False):
    grid = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    h = len(grid)
    w = len(grid[0])

    to_find = 'XMAS'
    for y in range(h):
        for x in range(w):
            if grid[y][x] == to_find[0]:
                for dx, dy in ddxy:
                    match = True
                    for i, ch in enumerate(to_find):
                        nx, ny = x + dx * i, y + dy * i
                        if 0 <= nx < w and 0 <= ny < h:
                            if ch != grid[ny][nx]:
                                match = False
                                break
                        else:
                            match = False
                            break
                    if match:
                        p1 += 1

    to_find_list = [
        {(0, 0): 'M', (2, 0): 'M', (1, 1): 'A', (0, 2): 'S', (2, 2): 'S'},
        {(0, 0): 'M', (2, 0): 'S', (1, 1): 'A', (0, 2): 'M', (2, 2): 'S'},
        {(0, 0): 'S', (2, 0): 'M', (1, 1): 'A', (0, 2): 'S', (2, 2): 'M'},
        {(0, 0): 'S', (2, 0): 'S', (1, 1): 'A', (0, 2): 'M', (2, 2): 'M'},
    ]
    for y in range(h - 3 + 1):
        for x in range(w - 3 + 1):
            for to_find in to_find_list:
                match = True
                for (dx, dy), ch in to_find.items():
                    nx, ny = x + dx, y + dy
                    if grid[ny][nx] != ch:
                        match = False
                        break
                if match:
                    p2 += 1
                    break

    return p1, p2


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', True, False, None],
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
