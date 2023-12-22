# DAY21

f = open('input/21.txt', 'r')
field = [list(line.strip()) for line in f.readlines()]

DIRS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

def find_start(field):
    w, h = len(field[0]), len(field)
    for j in range(h):
        for i in range(w):
            if field[j][i] == 'S':
                return i, j


def step(field, ppos):
    w, h = len(field[0]), len(field)
    res = set()
    for x, y in ppos:
        for dx, dy in DIRS:
            cx, cy = x + dx, y + dy
            if field[cy % h][cx % w] != '#':
                res.add((cx, cy))
    return res


def count_inside(ppos, xmin, xmax, ymin, ymax):
    return sum(x >= xmin and x <= xmax and y >= ymin and y <= ymax
               for x, y in ppos)


def step_times(field, n):
    sx, sy = find_start(field)
    ppos = set()
    ppos.add((sx, sy))
    for i in range(n):
        ppos = step(field, ppos)
    return ppos

def eval_pcount(ppos, side, nsteps):
    def count_in_square(x, y):
        return count_inside(ppos, x * side, (x + 1) * side - 1, y * side, (y + 1) * side - 1)

    # full squares odd/even
    nc1 = count_in_square(0, 0)
    nc2 = count_in_square(1, 0)

    # tip squares
    nt = count_in_square(0, -2)
    nl = count_in_square(-2, 0)
    nb = count_in_square(0, 2)
    nr = count_in_square(2, 0)

    # edge squares odd
    nlt1 = count_in_square(-1, -1)
    nrt1 = count_in_square(1, -1)
    nrb1 = count_in_square(1, 1)
    nlb1 = count_in_square(-1, 1)

    # ege squares even
    nlt2 = count_in_square(-2, -1)
    nrt2 = count_in_square(2, -1)
    nrb2 = count_in_square(2, 1)
    nlb2 = count_in_square(-2, 1)

    n = (nsteps - s0) // side

    res = nt + nl + nb + nr
    res += nc1 * ((n - 1) ** 2) + nc2 * (n ** 2)
    res += (nlt1 + nrt1 + nrb1 + nlb1) * (n - 1) + (nlt2 + nrt2 + nrb2 + nlb2) * n
    return res

ppos = step_times(field, 64)
res1 = len(ppos)
print(res1)

side = len(field)
s0 = side // 2
ppos = step_times(field, s0 + side * 2)

NSTEPS = 26501365
res2 = eval_pcount(ppos, side, NSTEPS)
print(res2)
