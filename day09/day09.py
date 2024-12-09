import time


def solve_puzzle(filename, param=None, verbose=False):
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]

    p1, p2 = 0, 0

    inp = [int(x) for x in lines[0]]
    disk = []
    disk2 = []
    for idx, n in enumerate(inp):
        if idx % 2 == 1:
            iD = -1
        else:
            iD = idx // 2
        disk2.append([iD, n])
        for _ in range(n):
            disk.append(iD)

    for ridx in range(len(disk) - 1, -1, -1):
        iD = disk[ridx]
        if iD != -1:
            for idx in range(len(disk)):
                if idx >= ridx:
                    break
                if -1 == disk[idx]:
                    disk[idx] = iD
                    disk[ridx] = -1
                    break

    p1 = sum([idx * iD for idx, iD in enumerate(disk) if iD != -1])

    changes = False
    ridx = len(disk2) - 1
    while ridx >= 0:
        iD, length = disk2[ridx]
        if iD != -1:
            for idx in range(len(disk2)):
                if idx >= ridx:
                    break
                iD2, length2 = disk2[idx]
                if iD2 == -1 and length2 >= length:
                    rem_length = length2 - length
                    disk2[idx] = [iD, length]
                    disk2[ridx] = [-1, length]
                    if rem_length > 0:
                        disk2.insert(idx + 1, [-1, rem_length])
                        ridx += 1
                    changes = True
                    break
        ridx -= 1
        if not changes:
            break

    idx = 0
    for iD, length in disk2:
        if iD != -1:
            for _ in range(length):
                p2 += idx * iD
                idx += 1
        else:
            idx += length

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
            print(p1)
            print(p2)
            print("%s \tin %d ms" % (description, round(1000 * (end - start), 2)))


if __name__ == '__main__':
    main()
