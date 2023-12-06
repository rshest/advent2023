# DAY03
f = open('input/03.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def is_symbol(c):
    return c is not None and not c.isdigit() and c != '.'


OFFSETS = [
    [-1, -1], [0, -1], [1, -1],
    [-1, 0], [1, 0],
    [-1, 1], [0, 1], [1, 1]]


def get_at(lines, x, y):
    h = len(lines)
    w = len(lines[0])
    if x >= 0 and x < w and y >= 0 and y < h:
        return lines[y][x]
    return None

def has_symbol_neighbor(lines, i, j):
    h = len(lines)
    w = len(lines[0])
    for dx, dy in OFFSETS:
        x = i + dx
        y = j + dy
        if is_symbol(get_at(lines, x, y)):
            return True
    return False

def get_gear_neighbors(lines, i, j):
    res = set()
    h = len(lines)
    w = len(lines[0])
    for dx, dy in OFFSETS:
        x = i + dx
        y = j + dy
        c = get_at(lines, x, y)
        if c == '*':
            res.add((x, y))
    return res

def extract_nums(lines):
    h = len(lines)
    w = len(lines[0])

    is_part = False
    n = 0
    num_digits = 0
    nums = []
    gears = set()
    for j in range(h):
        for i in range(w):
            c = lines[j][i]

            if c.isdigit():
                n = n * 10 + int(c)
                num_digits += 1
                is_part = is_part or has_symbol_neighbor(lines, i, j)
                g = get_gear_neighbors(lines, i, j)
                if g is not None:
                    gears = gears.union(g)

            if (not c.isdigit() or i == w - 1) and num_digits > 0:
                nums.append((n, is_part, gears))
                is_part = False
                n = 0
                num_digits = 0
                gears = set()
    return nums


def extract_gears(nums):
    gears = {}
    for _, _, gs in nums:
        for g in gs:
            if g in gears:
                gears[g] += 1
            else:
                gears[g] = 1

    gears = {g: 1 for g, count in gears.items() if count == 2}

    for n, is_part, gs in nums:
        for g in gs:
            if g in gears:
                gears[g] *= n
    return gears


nums = extract_nums(lines)
res1 = sum(n for n, is_part, _ in nums if is_part)
print(res1)

gears = extract_gears(nums)
res2 = sum(gears.values())
print(res2)
