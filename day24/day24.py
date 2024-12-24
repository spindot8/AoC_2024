import time
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


# see "The binary Full Adder"
# https://medium.com/@MarkEdwardMurray/binary-operations-and-xor-you-9417a5dc275d
#
# A, B, Cin as inputs. A and B are x00, y00 up to x44, y44, Cin is carry from previous stage (not present for x00, y00)
# S, Cout as outputs. S is z00 to z44, Cout is carry for next stage and z45 for most significant bit
#
#               ,---,         ,---,
# A (x03) ------|   |   |-----|   |
#               |XOR|---|     |XOR|--------------- S (z03)
# B (y03) ------| ^ |   | |---| ^ |
#               '---'   | |   '---'
#                       | |   ,---,
# Cin (Cin03) ------------|---|   |     ,---,
#                       |     |AND|-----|   |
#               ,___,   |-----| & |     |OR |----- Cout (Cin04)
# A (x03) ------|   |         '---'  ,--| | |
#               |AND|----------------'  '---'
# B (y03) ------| & |
#               '---'
def solve_puzzle(filename, param=None, verbose=False):
    groups = [[line.strip() for line in group.split('\n')] for group in open(filename, 'r').read().split('\n\n')]

    input_values = {}
    for y, line in enumerate(groups[0]):
        l, r = line.split(': ')
        r = int(r)
        input_values[l] = r

    target_ops = {}
    for y, line in enumerate(groups[1]):
        if len(line) == 0:
            continue
        s1, op, s2, _, t = line.split()
        target_ops[t] = [s1, op, s2]

    p1 = calc_result(target_ops, input_values)

    expected_value = get_expected_value(input_values)
    # print('expected target value', expected_value)
    orig_valid_count = check_z_outs(target_ops)

    swaps = set()
    for t1, ops1 in target_ops.items():
        for t2, ops2 in target_ops.items():
            if t1 == t2:
                continue
            target_ops[t1], target_ops[t2] = ops2, ops1
            valid_count = check_z_outs(target_ops)
            target_ops[t1], target_ops[t2] = ops1, ops2
            # print('swapping', t1, t2, valid_count, orig_valid_count)

            if valid_count > orig_valid_count:
                swaps.add(t1)
                swaps.add(t2)
                # print(len(swaps), swaps)

    sorted_swap_list = list(swaps)
    sorted_swap_list.sort()
    p2 = ','.join(sorted_swap_list)

    return p1, p2


def check_z_outs(target_ops):
    valid_count = 0
    for t in target_ops.keys():
        if t[0] == 'z':
            bit = int(t[1:])
            # print('check z outs', t, bit)
            if check_z_output(target_ops, bit):
                valid_count += 1
    return valid_count


def check_input_carry(t, target_ops, bit):
    a, op, b = target_ops[t]
    x = 'x{:02d}'.format(bit)
    y = 'y{:02d}'.format(bit)
    if op == 'AND' and ((a == x and b == y) or (a == y and b == x)):
        return True
    return False


def check_out_carry(t, target_ops, bit):
    a, op, b = target_ops[t]
    if op == 'AND':
        z = 'z{:02d}'.format(bit)
        a2, op2, b2 = target_ops[z]
        if (a == a2 or a == b2) and (b == b2 or b == a2) and op2 == 'XOR':
            return True
    return False


def check_carry(t, target_ops, bit):
    a, op, b = target_ops[t]
    if op == 'OR':
        if (check_input_carry(a, target_ops, bit-1) and check_out_carry(b, target_ops, bit-1)) or\
                (check_input_carry(b, target_ops, bit-1) and check_out_carry(a, target_ops, bit-1)):
            return True
    return False


def check_xor_input(t, target_ops, bit):
    if t in target_ops:
        a, op, b = target_ops[t]
        x = 'x{:02d}'.format(bit)
        y = 'y{:02d}'.format(bit)
        if op == 'XOR' and ((a == x and b == y) or (a == y and b == x)):
            return True
    return False


def check_z_output(target_ops, bit):
    t = 'z{:02d}'.format(bit)
    if t == 'z45':
        # last bit, just carry, assume correct
        return True
    elif t == 'z00':
        # first bit, no carry, assume correct
        return True
    else:
        a, op, b = target_ops[t]
        # print('check z output', bit, t, a, op, b)
        if op == 'XOR':
            if (check_xor_input(a, target_ops, bit) and check_carry(b, target_ops, bit)) or\
                    (check_xor_input(b, target_ops, bit) and check_carry(a, target_ops, bit)):
                return True
    return False


def calc_result(target_ops, values, highest_z=45, max_loop_count=300):
    ans = None

    loop = 0
    while True:
        loop += 1
        # print(loop)
        if loop >= max_loop_count:
            break

        for t, (s1, op, s2) in target_ops.items():
            if s1 in values and s2 in values:
                if op == 'AND':
                    values[t] = values[s1] & values[s2]
                elif op == 'OR':
                    values[t] = values[s1] | values[s2]
                elif op == 'XOR':
                    values[t] = values[s1] ^ values[s2]
                else:
                    assert False, op

        z_collected = {}
        for val in values.keys():
            if val[0] == 'z':
                z_collected[val] = values[val]
        # print(z_collected)
        if len(z_collected) == highest_z + 1:
            break

    if len(z_collected) == highest_z + 1:
        ans = get_bin_num(z_collected)
    return ans


def get_value(values, ch):
    collected = {}
    for k, v in values.items():
        if k[0] == ch:
            collected[k] = v
    ans = get_bin_num(collected)
    return ans


def get_expected_value(input_values):
    x = get_value(input_values, 'x')
    y = get_value(input_values, 'y')
    return x + y


def get_bin_num(collected):
    bits = ['0' for _ in range(len(collected))]
    for k, v in collected.items():
        idx = len(collected) - 1 - int(k[1:])
        bits[idx] = str(v)
        # print(k, v, idx, str(v))
    bits = ''.join(bits)
    ans = int(bits, 2)
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
            printc(p1)
            if p2:
                printc(p2)
            else:
                print(p2)
            print("%s \tin %d ms" % (description, round(1000 * (end - start), 2)))


if __name__ == '__main__':
    main()
