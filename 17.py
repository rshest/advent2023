%%time
# DAY17
import heapq

f = open('input/17.txt', 'r')
field = [line.strip() for line in f.readlines()]


def find_min_path(field, src, dst, min_steps, max_steps):
    w, h = len(field[0]), len(field)
    open = [(0, (src, 0, (0, 0)), src)]
    visited = {}
    while len(open) > 0:
        weight, node, prev = heapq.heappop(open)
        pos, steps, dir = node
        if node in visited and visited[node][0] != weight:
            continue
        x, y = pos
        px, py = prev
        next_dirs = []
        sx, sy = dir
        if steps >= min_steps or dir == (0, 0):
            if sy == 0:
                next_dirs += [(0, 1, 0), (0, -1, 0)]
            if sx == 0:
                next_dirs += [(-1, 0, 0), (1, 0, 0)]
        if steps < max_steps and dir != (0, 0):
            next_dirs += [(sx, sy, steps)]

        for dx, dy, csteps in next_dirs:
            cx, cy = x + dx, y + dy
            cpos = (cx, cy)
            if cx < 0 or cy < 0 or cx >= w or cy >= h:
                continue
            cw = weight + int(field[cy][cx])
            cnode = cpos, csteps + 1, (dx, dy)
            if cnode in visited and visited[cnode][0] <= cw:
                continue
            if cpos == dst and csteps + 1 < min_steps:
                continue
            heapq.heappush(open, (cw, cnode, pos))
            visited[cnode] = (cw, pos, steps)
    res = min(visited[key] for key in visited if key[0] == dst)
    return res[0]


w, h = len(field[0]), len(field)
res1 = find_min_path(field, (0, 0), (w - 1, h - 1), 0, 3)
print(res1)

res2 = find_min_path(field, (0, 0), (w - 1, h - 1), 4, 10)
print(res2)
