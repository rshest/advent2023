# DAY06
import math
from operator import mul
from functools import reduce

f = open('input/06.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_ints(line):
    return [int(x.strip()) for x in line.split()]

def parse_input(lines):
    t = parse_ints(lines[0].split(':')[1])
    d = parse_ints(lines[1].split(':')[1])
    return [(t[i], d[i]) for i in range(len(t))]

def get_roots_dist(t, d):
    det = t * t - 4 * d
    if det < 0:
        return 0
    ds = math.sqrt(det)
    r1 = math.ceil(0.5 * (ds + t))
    r2 = math.floor(0.5 * (t - ds))
    return abs(r1 - r2 - 1)

races = parse_input(lines)
dists = [get_roots_dist(t, d) for t, d in races]
res1 = reduce(mul, dists, 1)
print(res1)

lines2 = parse_input([l.replace(' ', '') for l in lines])
res2 = get_roots_dist(races2[0][0], races2[0][1])
print(res2)
