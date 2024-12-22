import time
from collections import defaultdict
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    results = defaultdict(int)
    for line in lines:
        n = int(line)
        prices = [n % 10]
        diffs = []
        for loop in range(2000):
            n = (n ^ (n * 64)) % 16777216
            n = (n ^ (n // 32)) % 16777216
            n = (n ^ (n * 2048)) % 16777216
            prices.append(n % 10)
            diffs.append(prices[-1] - prices[-2])
        p1 += n

        seen = set()
        for idx in range(3, len(diffs)):
            diff_seq = tuple(diffs[idx - 3:idx + 1])
            if diff_seq not in seen:
                seen.add(diff_seq)
                results[diff_seq] += prices[idx + 1]

    # print(len(results))
    p2 = max(results.values())

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
            printc(p1)
            if p2:
                printc(p2)
            else:
                print(p2)
            print("%s \tin %d ms" % (description, round(1000 * (end - start), 2)))


if __name__ == '__main__':
    main()
