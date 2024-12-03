import re
import time


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    prog = open(filename, 'r').read()

    p1, p2 = 0, 0

    enabled = True
    all_list = re.findall(r"(mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\))", prog)
    for txt in all_list:
        if txt.startswith('don'):
            enabled = False
        elif txt.startswith('do'):
            enabled = True
        else:
            assert txt.startswith('mul')
            a, b = nums(txt)
            p1 += a * b
            if enabled:
                p2 += a * b

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
