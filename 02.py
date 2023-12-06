# DAY02
f = open('input/02.txt', 'r')
lines = [line.strip() for line in f.readlines()]


def parse_turn(line):
    parts = line.split(',')
    res = [0, 0, 0]
    for p in parts:
        p = p.strip()
        n, color = p.split(' ')
        color = color.strip()
        if color == 'red':
            res[0] += int(n)
        if color == 'green':
            res[1] += int(n)
        if color == 'blue':
            res[2] += int(n)
    return res


def parse_line(line):
    line = line.split(': ')[1]
    return [parse_turn(t) for t in line.split(';')]


def is_game_possible(game, target):
    for r, g, b in game:
        if r > target[0] or g > target[1] or b > target[2]:
            return False
    return True


def get_min_target(game):
    min_r = max([r for r, _, _ in game])
    min_g = max([g for _, g, _ in game])
    min_b = max([b for _, _, b in game])
    return [min_r, min_g, min_b]


games = [parse_line(l) for l in lines]

TARGET = [12, 13, 14]

res1 = 0
for i in range(len(games)):
    if is_game_possible(games[i], TARGET):
        res1 += i + 1

print(res1)

min_targets = [get_min_target(g) for g in games]
res2 = sum(max(1, r) * max(1, g) * max(1, b) for r, g, b in min_targets)
print(res2)
