import re
import time


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1 = 0
    p2 = 0
    inp = []
    for y, line in enumerate(lines):
        inp.append(nums(line))

    for e in inp:
        safe = is_safe(e)
        if safe:
            p1 += 1
            p2 += 1
        else:
            for i in range(len(e)):
                ne = e[:i] + e[i + 1:]
                if is_safe(ne):
                    p2 += 1
                    break

    return p1, p2


def is_safe(e):
    all_inc = True
    all_dec = True

    prev = e[0]
    for n in e[1:]:
        diff_inc = prev - n
        diff_dec = n - prev
        if diff_inc < 1 or diff_inc > 3:
            all_inc = False
        if diff_dec < 1 or diff_dec > 3:
            all_dec = False
        prev = n

    return all_inc or all_dec


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
