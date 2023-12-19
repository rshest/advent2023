# DAY19
import re
from operator import mul
from functools import reduce

data = open('input/19.txt', 'r').read()

def parse_rule(line):
    p = line.split('{')
    name = p[0]
    conds = []
    for cp in p[1][:-1].split(','):
        lr = cp.split(':')
        if len(lr) == 1:
            conds.append((None, lr[0]))
        else:
            r, sign, n = re.split(r"(>|<)", lr[0])
            conds.append(((r, sign, int(n)), lr[1]))
    return name, conds


def parse_part(line):
    parts = []
    for p in line[1:-1].split(','):
        _, val = p.split('=')
        parts.append(int(val))
    return parts


def parse_data(data):
    parts = data.split('\n\n')
    p0 = dict(parse_rule(p) for p in parts[0].split('\n') if p != '')
    p1 = [parse_part(p) for p in parts[1].split('\n') if p != '']
    return p0, p1


PART_MAPPING = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3,
}

def eval_part(part, rules):
    rule = 'in'
    while True:
        for cond in rules[rule]:
            cmp, next = cond
            if cmp != None:
                r, sign, n = cmp
                val = part[PART_MAPPING[r]]
                if sign == '<' and val >= n:
                    continue
                elif sign == '>' and val <= n:
                    continue
            if next == 'A':
                return True
            elif next == 'R':
                return False
            else:
                rule = next
                break

def count_num_accepted_rec(rules, ranges, rule):
    if rule == 'A':
        return reduce(mul, [max(0, maxv - minv + 1) for minv, maxv in ranges], 1)
    elif rule == 'R':
        return 0
    cranges = [[minv, maxv] for minv, maxv in ranges]
    res = 0
    for cond in rules[rule]:
        cmp, next = cond
        if cmp != None:
            r, sign, n = cmp
            idx = PART_MAPPING[r]
            ranges1 = [[minv, maxv] for minv, maxv in cranges]
            if sign == '<':
                ranges1[idx][1] = min(ranges1[idx][1], n - 1)
                cranges[idx][0] = max(n, cranges[idx][0])
                res += count_num_accepted_rec(rules, ranges1, next)
            elif sign == '>':
                ranges1[idx][0] = max(ranges1[idx][0], n + 1)
                cranges[idx][1] = min(n, cranges[idx][1])
                res += count_num_accepted_rec(rules, ranges1, next)
        else:
            res += count_num_accepted_rec(rules, cranges, next)
    return res

def count_num_accepted(rules, minv, maxv):
    ranges = [[minv, maxv]] * 4
    return count_num_accepted_rec(rules, ranges, 'in')


rules, parts = parse_data(data)
res1 = sum(sum(p) for p in parts if eval_part(p, rules))
print(res1)

res2 = count_num_accepted(rules, 1, 4000)
print(res2)
