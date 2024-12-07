import re
import time


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    for idx, line in enumerate(lines):
        nums_in_line = nums(line)
        result = nums_in_line[0]
        numbers = nums_in_line[1:]
        if does_match(result, numbers, '+*', 0):
            p1 += result
        if does_match(result, numbers, '+*|', 0):
            p2 += result

    return p1, p2


def does_match(result, numbers, operators, value):
    if len(numbers) == 0:
        return result == value

    ans = False
    next_v = numbers[0]
    for op in operators:
        if op == '+':
            new_v = value + next_v
        elif op == '*':
            new_v = value * next_v
        else:
            assert op == '|'
            new_v = int(str(value) + str(next_v))

        if does_match(result, numbers[1:], operators, new_v):
            ans = True
            break

    return ans


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
