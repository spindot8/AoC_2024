import time
import itertools
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    inp = []
    for y, line in enumerate(lines):
        inp.append(int(line))

    prices_list = []
    diffs_list = []
    for n in inp:
        prices = [n % 10]
        for loop in range(2000):
            n = (n ^ (n * 64)) % 16777216
            n = (n ^ (n // 32)) % 16777216
            n = (n ^ (n * 2048)) % 16777216
            prices.append(n % 10)
        p1 += n
        prices_list.append(prices)
        diffs = [b - a for a, b in zip(prices, prices[1:])]
        diffs_list.append(diffs)

    possible_diffs = set()
    for diffs in diffs_list:
        for idx in range(3, len(diffs)):
            possible_diffs.add(tuple(diffs[idx - 3:idx + 1]))
    # print(len(possible_diffs))
    # print(len(list(itertools.product([n for n in range(-9, 10)], repeat=4))))

    pre_process_diffs_list = []
    for m, diff in enumerate(diffs_list):
        pre_process_diff = {}
        for idx in range(3, len(diff)):
            cdiff = tuple(diff[idx - 3:idx + 1])
            if cdiff not in pre_process_diff:
                pre_process_diff[cdiff] = prices_list[m][idx + 1]
        pre_process_diffs_list.append(pre_process_diff)

    for pd in possible_diffs:
        ans = 0
        for pre_process_diffs in pre_process_diffs_list:
            if pd in pre_process_diffs:
                ans += pre_process_diffs[pd]
        if ans > p2:
            # print(ans, pd)
            p2 = ans

    return p1, p2


def main():
    input_data_list = [
        ['sample.txt',  'sample data  ', False, False, None],
        # takes about 30 seconds
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
