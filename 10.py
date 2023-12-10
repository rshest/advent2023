# DAY10

f = open('input/10.txt', 'r')
field = [line.strip() for line in f.readlines()]

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
SYMS = {
    '|': [(0, -1), (0, 1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, -1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(0, 1), (-1, 0)],
    'F': [(0, 1), (1, 0)],
}


def find_start(field):
    w = len(field[0])
    h = len(field)
    for j in range(h):
        for i in range(w):
            if field[j][i] == 'S':
                return i, j


def find_next(field, start):
    w, h = len(field[0]), len(field)
    x, y = start
    for dx, dy in DIRS:
        px, py = x + dx, y + dy
        if px < 0 or px >= w or py < 0 or py >= h:
            continue
        c = field[py][px]
        if not c in SYMS:
            continue
        for kx, ky in SYMS[c]:
            nx, ny = px + kx, py + ky
            if (nx, ny) == (x, y):
                yield px, py


def get_sym(field, pos):
    x, y = pos
    c = field[y][x]
    if c != 'S':
        return c
    adj = sorted([(px - x, py - y) for px, py in find_next(field, pos)])
    for k, v in SYMS.items():
        if adj == sorted(v):
            return k


def traverse(field):
    w, h = len(field[0]), len(field)
    prev = find_start(field)
    x, y = list(find_next(field, prev))[0]
    yield prev
    while True:
        c = field[y][x]
        for dx, dy in SYMS[c]:
            px, py = x + dx, y + dy
            if (px, py) != prev:
                prev = x, y
                x, y = px, py
                break
        yield prev
        if field[y][x] == 'S' or (x, y) == prev:
            return


def get_inside(field, path):
    w, h = len(field[0]), len(field)
    spath = set(path)
    for j in range(h):
        inside = False
        i = 0
        while i < w:
            c = get_sym(field, (i, j))
            if (i, j) in spath:
                if c == '|':
                    inside = not inside
                elif c == 'F':
                    inside = not inside
                    while get_sym(field, (i, j)) not in ['J', '7']:
                        i += 1
                    if get_sym(field, (i, j)) == '7':
                        inside = not inside
                elif c == 'L':
                    inside = not inside
                    while get_sym(field, (i, j)) not in ['J', '7']:
                        i += 1
                    if get_sym(field, (i, j)) == 'J':
                        inside = not inside
            else:
                if inside:
                    yield i, j
            i += 1


path = [p for p in traverse(field)]
res1 = int(len(path) / 2)
print(res1)

inside = list(get_inside(field, path))
res2 = len(inside)
print(res2)

def draw_field(field, path, inside):
    SUBST = {
        '|': '│',
        '-': '─',
        'L': '└',
        'J': '┘',
        '7': '┐',
        'F': '┌',
    }
    spath = set(path)
    sinside = set(inside)
    for j in range(len(field)):
        line = field[j]
        chars = [c for c in line]
        for i in range(len(chars)):
            c = chars[i]
            if c == 'S':
                continue
            if (i, j) not in spath:
                chars[i] = '█' if (i, j) in sinside else ' '
            else:
                chars[i] = SUBST[c]
        print(''.join(chars))

draw_field(field, path, inside)
