# DAY16
f = open('input/16.txt', 'r')
field = [line.strip() for line in f.readlines()]

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def trace_ray(field, pos, dir, visited):
    w, h = len(field[0]), len(field)
    x, y = pos
    while (x, y, dir) not in visited:
        c = field[y][x]
        visited.add((x, y, dir))
        if c == '-':
            if dir in [1, 3]:
                trace_ray(field, (x, y), 0, visited)
                dir = 2
        elif c == '|':
            if dir in [0, 2]:
                trace_ray(field, (x, y), 1, visited)
                dir = 3
        elif c == '\\':
            dir = [1, 0, 3, 2][dir]
        elif c == '/':
            dir = [3, 2, 1, 0][dir]
        dx, dy = DIRS[dir]
        x, y = x + dx, y + dy
        if x < 0 or y < 0 or x >= w or y >= h:
            break


def get_num_visited(field, pos, dir):
    visited = set()
    trace_ray(field, pos, dir, visited)
    return len(set((x, y) for x, y, _ in visited))


res1 = get_num_visited(field, (0, 0), 0)
print(res1)

res2 = 0
w, h = len(field[0]), len(field)
for i in range(w):
    res2 = max(res2, get_num_visited(field, (i, 0), 1))
    res2 = max(res2, get_num_visited(field, (i, h - 1), 3))
for i in range(h):
    res2 = max(res2, get_num_visited(field, (0, i), 0))
    res2 = max(res2, get_num_visited(field, (w - 1, i), 2))
print(res2)
