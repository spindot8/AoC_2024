import time
from collections import *
import networkx as nx
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    con = defaultdict(set)
    for y, line in enumerate(lines):
        l, r = line.split('-')
        con[l].add(r)
        con[r].add(l)

    G = nx.Graph()
    for comp, values in con.items():
        for v in values:
            G.add_edge(comp, v)

    max_len = max(len(clique) for clique in nx.enumerate_all_cliques(G))
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) == 3 and any(v[0] == 't' for v in clique):
            p1 += 1
        if len(clique) == max_len:
            p2 = ','.join(sorted(list(clique)))

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
