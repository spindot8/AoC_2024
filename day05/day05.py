import re
import time


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    groups = [[line.strip() for line in group.split('\n')] for group in open(filename, 'r').read().split('\n\n')]

    p1, p2 = 0, 0

    rules = set()
    for y, line in enumerate(groups[0]):
        a, b = nums(line)
        rules.add((a, b))

    prints = []
    for y, line in enumerate(groups[1]):
        if len(line) == 0:
            continue
        prints.append(nums(line))

    for pages in prints:
        valid, idx1, idx2 = check_valid(pages, rules)
        if valid:
            p1 += get_score(pages)
        else:
            while True:
                if not valid:
                    v1, v2 = pages[idx1], pages[idx2]
                    pages[idx1] = v2
                    pages[idx2] = v1
                    valid, idx1, idx2 = check_valid(pages, rules)
                else:
                    break
            p2 += get_score(pages)

    return p1, p2


def get_score(pages):
    return pages[len(pages) // 2]


def check_valid(pages, rules):
    valid = True
    idx1, idx2 = 0, 0
    for i, page in enumerate(pages):
        for idx in range(i + 1, len(pages)):
            page2 = pages[idx]
            if (page, page2) not in rules:
                assert (page2, page) in rules
                idx1 = i
                idx2 = idx
                valid = False
                break
        if not valid:
            break
        for idx in range(0, i):
            page0 = pages[idx]
            if (page0, page) not in rules:
                idx1 = idx
                idx2 = i
                valid = False
                break
        if not valid:
            break
    return valid, idx1, idx2


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
