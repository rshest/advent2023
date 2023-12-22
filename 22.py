# DAY22
import sys

f = open('input/22.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_coord(line):
    parts = line.split('~')
    c1 = tuple(map(int, parts[0].split(',')))
    c2 = tuple(map(int, parts[1].split(',')))
    if c1[2] > c2[2]:
        c1, c2 = c2, c1
    return c1, c2


def enum_points(p1, p2):
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    x1, x2 = (x2, x1) if x2 < x1 else (x1, x2)
    y1, y2 = (y2, y1) if y2 < y1 else (y1, y2)
    z1, z2 = (z2, z1) if z2 < z1 else (z1, z2)
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                yield (x, y, z)


def compact(coords):
    profile = {}
    res = []
    for p1, p2 in coords:
        (x1, y1, z1), (x2, y2, z2) = p1, p2
        zoffs = sys.maxsize
        for x, y, z in enum_points(p1, p2):
            pz =  profile[(x, y)] if (x, y) in profile else 0
            zoffs = min(z - pz - 1, zoffs)
        res.append(((x1, y1, z1 - zoffs), (x2, y2, z2 - zoffs)))
        for x, y, z in enum_points(p1, p2):
            profile[(x, y)] = z - zoffs
    return res


def find_supported(coords):
    profile = {}
    nc = len(coords)
    res = [set() for _ in range(nc)]
    for i in range(nc):
        p1, p2 = coords[i]
        (x1, y1, z1), (x2, y2, z2) = p1, p2
        for x, y, z in enum_points(p1, p2):
            if (x, y) in profile:
                pz, pidx = profile[(x, y)]
                if pz + 1 == z and pidx != i:
                    res[i].add(pidx)
            profile[(x, y)] = (z, i)
    return res


def find_all_supported(idx, sup):
    moved = [False for _ in range(len(sup))]
    moved[idx] = True
    for i in range(idx + 1, len(sup)):
        if len(sup[i]) > 0 and all(moved[x] for x in sup[i]):
            moved[i] = True
    return sum(moved) - 1


coords = [parse_coord(line) for line in lines]
coords = sorted(coords, key=lambda p: p[0][2])

coords = compact(coords)
sup = find_supported(coords)
critical = set(x for s in sup for x in s if len(s) == 1)
res1 = len(coords) - len(critical)
print(res1)

res2 = sum(find_all_supported(x, sup) for x in range(len(sup)))
print(res2)
