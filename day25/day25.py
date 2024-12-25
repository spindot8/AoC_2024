import time
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    groups = [[line.strip() for line in group.split('\n')] for group in open(filename, 'r').read().split('\n\n')]

    p1, p2 = 0, 0

    locks = []
    keys = []
    for lines in groups:
        grid = set()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == '#':
                    grid.add((x, y))
        if (0, 0) in grid:
            locks.append(grid)
        else:
            keys.append(grid)

    for key in keys:
        for lock in locks:
            fit = key | lock
            if len(fit) == len(lock) + len(key):
                p1 += 1

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
            printc(p1)
            if p2:
                printc(p2)
            else:
                print(p2)
            print("%s \tin %d ms" % (description, round(1000 * (end - start), 2)))


if __name__ == '__main__':
    main()
