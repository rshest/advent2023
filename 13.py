# DAY13
data = open('input/13.txt', 'r').read()


def parse_field(data):
    lines = data.strip().split('\n')
    return [list(line) for line in lines]


def transpose(field):
    w = len(field[0])
    h = len(field)
    res = [[' '] * h for _ in range(w)]
    for j in range(h):
        for i in range(w):
            res[i][j] = field[j][i]
    return res


def find_mirrors(field):
    w = len(field[0])
    h = len(field)
    hashes = [0] * h
    hreg = {}
    for j in range(h):
        ch = hash("".join(field[j]))
        if ch in hreg and hreg[ch] != field[j]:
            raise ValueError('Hash collision!!!')
        hashes[j] = ch
        hreg[ch] = field[j]
    for j in range(h - 1):
        n = 0
        while j - n >= 0 and j + n < h - 1 and hashes[j - n] == hashes[j + 1 + n]:
            n += 1
        if n == min(j + 1, h - j - 1):
            yield j + 1


def eval_reflections(fields):
    res = 0
    for f in fields:
        s1 = 100 * sum(s for s in find_mirrors(f))
        s2 = sum(s for s in find_mirrors(transpose(f)))
        res += s1 + s2
    return res


def flip_cell(field, x, y):
    c = field[y][x]
    field[y][x] = '#' if c == '.' else '.'


def fix_smudge(field):
    w = len(field[0])
    h = len(field)
    tfield = transpose(field)
    hlines = set(find_mirrors(field))
    vlines = set(find_mirrors(tfield))
    for j in range(h):
        for i in range(w):
            flip_cell(field, i, j)
            flip_cell(tfield, j, i)
            hlines1 = set(find_mirrors(field))
            vlines1 = set(find_mirrors(tfield))
            if len(hlines1) + len(vlines1) > 0 and (hlines != hlines1 or vlines != vlines1):
                yield hlines1.difference(hlines), vlines1.difference(vlines)
            flip_cell(field, i, j)
            flip_cell(tfield, j, i)


fields = [parse_field(p) for p in data.split('\n\n')]

res1 = eval_reflections(fields)
print(res1)

res2 = 0
for f in fields:
    hlines, vlines = list(fix_smudge(f))[0]
    s1 = 100 * sum(list(hlines))
    s2 = sum(list(vlines))
    res2 += s1 + s2
print(res2)
