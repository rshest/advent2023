# DAY14
f = open('input/14.txt', 'r')
field = [list(line.strip()) for line in f.readlines()]


def tilt_v(field, dir):
    w, h = len(field[0]), len(field)
    offs = [0] * w
    for j in range(h) if dir == -1 else range(h - 1, -1, -1):
        for i in range(w):
            c = field[j][i]
            if c == '.':
                offs[i] += 1
            elif c == '#':
                offs[i] = 0
            elif c == 'O':
                field[j][i] = '.'
                field[j + dir * offs[i]][i] = 'O'


def tilt_h(field, dir):
    w, h = len(field[0]), len(field)
    offs = [0] * h
    for j in range(h):
        for i in range(w) if dir == -1 else range(w - 1, -1, -1):
            c = field[j][i]
            if c == '.':
                offs[j] += 1
            elif c == '#':
                offs[j] = 0
            elif c == 'O':
                field[j][i] = '.'
                field[j][i + dir * offs[j]] = 'O'


def cycle(field):
    tilt_v(field, -1)
    tilt_h(field, -1)
    tilt_v(field, 1)
    tilt_h(field, 1)


def cycle_times(field, iters):
    history = {}
    rem = 0
    for i in range(iters):
        key = hash("".join("".join(p) for p in field))
        if key in history:
            # found loop
            start = history[key]
            rem = (iters - start) % (i - start)
            break
        cycle(field)
        history[key] = i

    for i in range(rem):
        cycle(field)


def compute_load(field):
    w, h = len(field[0]), len(field)
    res = 0
    for j in range(h):
        for i in range(w):
            c = field[j][i]
            if c == 'O':
                res += h - j
    return res


field1 = [row[:] for row in field]
tilt_v(field1, -1)
res1 = compute_load(field1)
print(res1)

cycle_times(field, 1000000000)
res2 = compute_load(field)
print(res2)
