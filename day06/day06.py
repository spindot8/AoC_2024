import time


#       NORTH    EAST    SOUTH   WEST
#       UP       RIGHT   DOWN    LEFT
dxy = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    gx, gy = 0, 0
    grid = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == '^':
                gx, gy = x, y
                ch = '.'
            grid[(x, y)] = ch

    p1, walked_fields, _ = walk_the_grid(grid, gx, gy, 0)

    p2 = 0
    for x, y in walked_fields:
        if x == gx and y == gy:
            continue

        ch = grid[(x, y)]
        if ch == '.':
            grid[(x, y)] = '#'
            _, _, endless = walk_the_grid(grid, gx, gy, 0)
            if endless:
                p2 += 1

            grid[(x, y)] = '.'

    return p1, p2


def walk_the_grid(grid, gx, gy, gd):
    fields = set()
    seen = set()
    x, y, d = gx, gy, gd
    while True:
        if (x, y, d) in seen:
            endless = True
            break
        seen.add((x, y, d))
        fields.add((x, y))

        dx, dy = dxy[d]
        nx, ny = x + dx, y + dy
        if (nx, ny) in grid:
            nch = grid[(nx, ny)]
            if nch == '#':
                d = (d+1) % 4
            else:
                x, y = nx, ny
        else:
            endless = False
            break
    return len(fields), fields, endless


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, None],
        # takes about 5 seconds
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
