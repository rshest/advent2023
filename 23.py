import threading
import sys

f = open('input/23.txt', 'r')
field = [line.strip() for line in f.readlines()]

DIRS = {'v': (0, 1), '>': (1, 0), '<': (-1, 0), '^': (0, -1)}


def find_longest_path_len(field, pos, dst, visited, cur_max, use_slopes=True, dist = 0):
    if pos == dst:
        res = max(len(visited), cur_max)
        return res
    x, y = pos
    c = field[y][x]
    visited.add(pos)
    dirs = DIRS.values()
    if use_slopes and c != '.':
        dirs = [DIRS[c]]
    for dx, dy in dirs:
        cx, cy = x + dx, y + dy
        cpos = cx, cy
        cc = field[cy][cx]
        if cc != '#' and cpos not in visited:
            cur_max = find_longest_path_len(field, cpos, dst, visited, cur_max, use_slopes, dist + 1)
    visited.remove(pos)
    return cur_max


def get_junction_graph(field, src, dst):
    res = {src: set()}
    def traverse(pos, prev, lastj, depth):
        if pos == dst:
            res[lastj].add((pos, depth))
            return
        x, y = pos
        c = field[y][x]
        dirs = []
        for dx, dy in DIRS.values():
            cx, cy = x + dx, y + dy
            cpos = cx, cy
            cc = field[cy][cx]
            if cc != '#' and cpos != prev:
                dirs.append((dx, dy))
        is_junction = len(dirs) > 1
        if is_junction:
            res[lastj].add((pos, depth))
            if pos in res:
                return
            res[pos] = set()
            res[pos].add((lastj, depth))
            lastj = pos
            depth = 0
        for dx, dy in dirs:
            traverse((x + dx, y + dy), pos, lastj, depth + 1)
    traverse(src, src, src, 0)
    return res


def find_path(graph, node, dst, visited, cur_max):
    if node == dst:
        return cur_max
    visited.add(node)
    res = 0
    for nnode, nw in graph[node]:
        if nnode not in visited:
            res = max(res, find_path(graph, nnode, dst, visited, cur_max + nw))
    visited.remove(node)
    return res


w, h = len(field[0]), len(field)
src, dst = (1, 0), (w - 2, h - 1)
res1 = find_longest_path_len(field, src, dst, set(), 0, True)
print(res1)

threading.stack_size(10**8)
sys.setrecursionlimit(w * h)

g2 = None
class RunThread(threading.Thread):
  def run(self):
    global g2
    g2 = get_junction_graph(field, src, dst)

rthread = RunThread()
rthread.start()
rthread.join()

res2 = find_path(g2, src, dst, set(), 0)
print(res2)
