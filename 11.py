f = open('input/11.txt', 'r')
lines = [line.strip() for line in f.readlines()]


def parse_field(lines):
    h = len(lines)
    w = len(lines[0])
    res = set()
    for j in range(h):
        for i in range(w):
            if lines[j][i] == '#':
                res.add((i, j))
    return res


def manhattan_dist(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def expand_field(field, factor=2):
    sf = sorted(field)
    res = set()
    lastx = sf[0][0]
    delta = 0
    for x, y in sf:
        if x - lastx > 1:
            delta += (factor - 1) * (x - lastx - 1)
        res.add((x + delta, y))
        lastx = x
    return res


def swap_coords(field):
    res = set()
    for x, y in field:
        res.add((y, x))
    return res


def get_dists(field):
    coords = list(field)
    nc = len(coords)
    res = 0
    for i in range(nc):
        for j in range(i + 1, nc):
            res += manhattan_dist(coords[i], coords[j])
    return res


def solve(field, factor=2):
    field = expand_field(field, factor)
    field = swap_coords(expand_field(swap_coords(field), factor))
    return get_dists(field)


field = parse_field(lines)
res1 = solve(field)
print(res1)

res2 = solve(field, 1000000)
print(res2)
