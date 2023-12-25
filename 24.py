# DAY24
import math

EPS = 0.0000000000001

TEST = True
f = open(f"input/24{'_test' if TEST else ''}.txt", 'r')
lines = [line.strip() for line in f.readlines()]

def parse_param(line):
    parts = line.split('@')
    return tuple(tuple(list(map(int, p.split(',')))) for p in parts)


def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add(a, b):
     return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def sub(a, b):
     return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def mulvs(a, s):
    return a[0] * s, a[1] * s, a[2] * s


def norm(a):
    return dot(a, a)


def normalize(a):
    d = math.sqrt(norm(a))
    return a[0] / d, a[1] / d, a[2] / d


def roundv(a):
    return round(a[0]), round(a[1]), round(a[2])


def dist(a, b):
    return math.sqrt(norm(sub(a, b)))


def plane_from_parallel_lines(line1, line2):
    p1, n1 = line1
    p2, n2 = line2
    v2 = normalize(cross(n2, normalize(sub(p1, p2))))
    return p2, v2


def plane_line_intersection(plane, line):
    pp, pn = plane
    pl, ln = line
    d = dot(pn, ln)
    if d == 0:
        return None
    d1 = dot(sub(pp, pl), pn) / d
    return add(pl, mulvs(ln, d1))


def line_intersection_xy(ray1, ray2):
    (x1, y1, z1), (p1, q1, r1) = ray1
    (x2, y2, z2), (p2, q2, r2) = ray2

    d = p2 * q1 - p1 * q2
    if abs(d) == 0:
        return None
    t1 = (q2 * x1 - q2 * x2 - p2 * y1 + p2 * y2) / d
    t2 = (q1 * x1 - q1 * x2 - p1 * y1 + p1 * y2) / d
    return (t1, t2), (x1 + t1 * p1, y1 + t1 * q1, z1 + t1 * r1)


def in_bounds(xstatus, bounds):
    if xstatus is None:
        return False
    (t1, t2), p = xstatus
    if t1 < 0 or t2 < 0:
        return False
    b1, b2 = bounds
    x, y, _ = p
    return x >= b1 and x <= b2 and y >= b1 and y <= b2


def is_point_on_line(pt, line):
    d = sub(pt, line[0])
    print(dot(d, line[1]) ** 2, norm(d))
    return abs(dot(d, line[1]) ** 2 - norm(d)) < EPS


def find_num_intersections_xy(param):
    res = 0
    for i in range(len(param)):
        for j in range(i + 1, len(param)):
            xs = line_intersection_xy(param[i], param[j])
            res += in_bounds(xs, BOUNDS)
    return res


param = list(map(parse_param, lines))

BOUNDS = (7, 27) if TEST else (200000000000000, 400000000000000)
res1 = find_num_intersections_xy(param)
print(res1)

planes = []
for i in range(len(param)):
        for j in range(i + 1, len(param)):
            xs = line_intersection_xy(param[i], param[j])
            if xs == None:
                plane = plane_from_parallel_lines(param[i], param[j])
                planes.append(plane)

# this assumes that there are at least two parallel lines in the input
xpts = []
for p in param:
    px = plane_line_intersection(planes[0], p)
    if px != None:
        xpts.append(px)

v1 = sub(xpts[1], xpts[0])
line = xpts[0], v1

ts = []
for p in param[:2]:
    xs = line_intersection_xy(p, line)
    ps, pn = p
    (t1, t2), px = xs
    ts.append((t1, t2, px))
ts = sorted(ts)

idx0 = 0
idx1 = -1
scale = (ts[idx1][0] - ts[idx0][0]) / (ts[idx1][1] - ts[idx0][1])
offs = ts[idx0][0] - ts[idx0][1] * scale

nres = roundv(mulvs(line[1], 1.0 / scale))
pres = roundv(sub(ts[idx0][2], mulvs(nres, ts[idx0][0])))
res2 = sum(pres)
print(res2)
