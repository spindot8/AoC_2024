import time
from collections import *
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def check_connections(con: dict, comp: str, found: set, ans: set):
    sorted_found = tuple(sorted(list(found)))
    if sorted_found not in ans:
        ans.add(sorted_found)
        for comp_to_check in con[comp]:
            if comp_to_check in found:
                continue
            all_con = True
            for connected_comp in found:
                if comp_to_check not in con[connected_comp]:
                    all_con = False
                    break
            if all_con:
                new_found = set(found)
                new_found.add(comp_to_check)
                check_connections(con, comp_to_check, new_found, ans)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    comps = set()
    con = defaultdict(set)
    for y, line in enumerate(lines):
        l, r = line.split('-')
        con[l].add(r)
        con[r].add(l)
        comps.add(l)
        comps.add(r)

    ans = set()
    for comp in comps:
        found = {comp}
        check_connections(con, comp, found, ans)
    # print(len(ans))
    # cnt = dict(Counter([len(con) for con in ans]))
    # print(cnt)

    p1_unique = set()
    max_len = max(len(con) for con in ans)
    for con in ans:
        if len(con) == 3:
            p1_unique.add(con)
        if len(con) == max_len:
            p2 = ','.join(con)

    for unique3 in p1_unique:
        if any(v[0] == 't' for v in unique3):
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
