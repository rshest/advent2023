# DAY08
import math
import functools

f = open('input/08.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_node(line):
    parts = line.split(' = ')
    return parts[0], parts[1][1:-1].split(', ')

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def get_nsteps(n='AAA', lastz=True):
    i = 0
    while True:
        s = dirs[i % len(dirs)]
        idx = 0 if s == 'L' else 1
        n = nodes[n][idx]
        i += 1
        if (not lastz and n == 'ZZZ') or (lastz and n[-1] == 'Z'):
            return i

dirs = lines[0]
nodes = [parse_node(line) for line in lines[2:]]
nodes = {n: lr for n, lr in nodes}

res1 = get_nsteps('AAA', False)
print(res1)

start_nodes = [x for x in nodes.keys() if x[-1] == 'A']
nsteps = [get_nsteps(n, True) for n in start_nodes]
res2 = functools.reduce(lambda a, b: lcm(a, b), nsteps)
print(res2)
