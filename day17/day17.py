import re
import time
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def load_program(filename):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    a = nums(lines[0])[0]
    b = nums(lines[1])[0]
    c = nums(lines[2])[0]
    instr = nums(lines[4])
    # print(a, b, c, instr)
    return a, b, c, instr


def run_prog(instr, a, b=0, c=0):
    def get_combo(op):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return a
        elif op == 5:
            return b
        elif op == 6:
            return c
        else:
            assert False, op

    output = []
    idx = 0
    while idx < len(instr):
        cmd = instr[idx]
        idx += 1
        op = instr[idx]
        idx += 1

        if cmd == 0:
            v = 2 ** get_combo(op)
            a //= v
        elif cmd == 1:
            b ^= op
        elif cmd == 2:
            b = (get_combo(op) % 8)
        elif cmd == 3:
            if a != 0:
                idx = op
        elif cmd == 4:
            b ^= c
        elif cmd == 5:
            output.append(get_combo(op) % 8)
        elif cmd == 6:
            v = 2 ** get_combo(op)
            b = a // v
        elif cmd == 7:
            v = 2 ** get_combo(op)
            c = a // v
        else:
            assert False, (cmd, op, idx)

    return output


def run_my_prog(a):
    output = []
    while a > 0:
        a_mod_8_xor_1 = ((a % 8) ^ 1)
        out = ((a_mod_8_xor_1 ^ 5) ^ (a // (2 ** a_mod_8_xor_1))) % 8
        a //= 8
        output.append(out)
    return output


def solve_puzzle(filename, param=None, verbose=False):
    a, _, _, instr = load_program(filename)

    output = run_prog(instr, a)
    # output_2 = run_my_prog(a)
    # assert output == output_2, (output, output_2)
    p1 = ','.join([str(n) for n in output])

    # this seems to be valid for every input data, it assumes that instruction 0 with operand 3 occurs
    a_multiply = 8

    target = list(instr)
    target.reverse()

    current_a = 0
    idx = 0
    p2 = 0
    while idx < len(target):
        add_a = 0
        while True:
            a = current_a + add_a
            output = run_prog(instr, a)
            rev_out = list(output)
            rev_out.reverse()
            if rev_out == target[:len(output)]:
                current_a = a * a_multiply
                # print('found', a, current_a, idx, output)
                p2 = a
                idx += 1
                break
            add_a += 1

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
