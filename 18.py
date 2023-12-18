# DAY18

f = open('input/18.txt', 'r')
lines = [line.strip() for line in f.readlines()]

DIRS = {
    'U': ((0, -1), (0, 0)),
    'R': ((1, 0), (0, 0)),
    'D': ((0, 1), (1, 0)),
    'L':  ((-1, 0), (0, 1)),
}

def parse_line(line):
    parts = line.translate({ord(i): None for i in '#()'}).split()
    return tuple(parts)


def trace(cmds):
    res = [(0, 0)]
    x, y = 0, 0
    for dir, n, _ in cmds:
        (dx, dy), (lx, ly) = DIRS[dir]
        dist = int(n)
        x, y = x + dx * dist, y + dy * dist
        ex, ey = x + lx, y + ly
        # expand previous point to cell boundaries as well
        px, py = res[-1]
        if px == x:
            px = ex
        if py == y:
            py = ey
        res[-1] = px, py
        res.append((ex, ey))
    return res


def translate_cmds(cmds):
    res = []
    for _, _, clr in cmds:
        dir = "RDLU"[int(clr[-1])]
        dist = int(clr[:-1], 16)
        res.append((dir, dist, clr))
    return res


def scan_points(points):
    hsegs = []
    np = len(points)
    for i in range(0, np - 1):
        p1 = points[i]
        p2 = points[(i + 1) % np]
        if p1[1] == p2[1]:
            hsegs.append((p1, p2))

    pts = []
    for i in range(len(hsegs)):
        p1, p2 = hsegs[i]
        px1, px2 = p1[0], p2[0]
        if px1 > px2:
            px1, px2 = px2, px1
        pts.append((px1, i + 1))
        pts.append((px2, -(i + 1)))
    pts = sorted(pts)

    res = 0
    prevx = pts[0][0]
    ycoords = set()
    for x, id in pts:
        y = hsegs[abs(id) - 1][0][1]
        if x != prevx:
            i = 0
            yy = sorted(list(ycoords))
            while i < len(yy):
                res += (x - prevx) * (yy[i + 1] - yy[i])
                i += 2
        if id > 0:
            ycoords.add(y)
        else:
            ycoords.remove(y)
        prevx = x
    return res


cmds = [parse_line(line) for line in lines]
points = trace(cmds)
res1 = scan_points(points)
print(res1)

points = trace(translate_cmds(cmds))
res2 = scan_points(points)
print(res2)
