import re
import time
import pyperclip


# print the supplied value and paste it to the clipboard
def printc(value):
    print(value)
    pyperclip.copy(value)


def nums(line):
    return [int(x) for x in re.findall(r'[0-9]+', line)]


def solve_puzzle(filename, param=None, verbose=False):
    groups = [[line.strip() for line in group.split('\n')] for group in open(filename, 'r').read().split('\n\n')]

    p1, p2 = 0, 0

    games = []
    for group in groups:
        game = []
        for y, line in enumerate(group):
            if len(line) == 0:
                continue
            game.append(tuple(nums(line)))
        games.append(tuple(game))

    for idx, game in enumerate(games):
        ans = play_game_math(game)
        if ans is not None:
            p1 += ans

        (ax, ay), (bx, by), (px, py) = game
        new_game = ((ax, ay), (bx, by), (10000000000000 + px, 10000000000000 + py))
        ans = play_game_math(new_game)
        if ans is not None:
            p2 += ans

    return p1, p2


def play_game_math(game):
    ans = None
    (ax, ay), (bx, by), (px, py) = game
    # print('x *', ax, '+ y * ', bx, '=', px, 'and', 'x *', ay, '+ y * ', by, '=', py)

    # first equation resolved to x put into second equation and resolved to y
    y = ((py * ax) - (px * ay)) / ((by * ax) - (bx * ay))
    # result of y put into first equation resolved to x
    x = (px - y * bx) / ax

    ans_a, ans_b = int(x), int(y)
    ans_x = ans_a * ax + ans_b * bx
    ans_y = ans_a * ay + ans_b * by

    if ans_x == px and ans_y == py:
        ans = ans_a * 3 + ans_b * 1
        # print(x, y, ans_a, ans_b, ans_x, ans_y, px, py, ans)
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
