import time
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    patterns = lines[0].split(', ')

    towels = []
    for y, line in enumerate(lines[2:]):
        towels.append(line)

    for n, towel in enumerate(towels):
        cache = {}
        cnt = match_towel(towel, '', cache, patterns)
        if cnt > 0:
            p1 += 1
            p2 += cnt

    return p1, p2


def match_towel(towel, pattern, cache, patterns):
    if pattern == towel:
        return 1

    cache_key = (towel, pattern)
    if cache_key in cache:
        return cache[cache_key]

    count = 0
    for np in patterns:
        new_pattern = pattern + np
        if towel.startswith(new_pattern):
            count += match_towel(towel, new_pattern, cache, patterns)

    cache[cache_key] = count
    return count


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
