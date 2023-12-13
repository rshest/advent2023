f = open('input/12.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_line(line):
    parts = line.split()
    return list(parts[0]), [int(x.strip()) for x in parts[1].strip().split(",")]

def get_num_subst(syms, ranges, mem, syms_offs=0, range_offs=0, cont=False):
    nr = len(ranges)
    if syms_offs == len(syms):
        if range_offs == nr or (range_offs == nr - 1 and
                                ranges[range_offs] == 0):
            return 1
        else:
            return 0
    c = syms[syms_offs]
    key = (syms_offs, range_offs, -1 if not cont or range_offs >= nr else ranges[range_offs], c)
    if key in mem:
        return mem[key]

    res = 0
    if c == '#':
        if range_offs == nr or ranges[range_offs] == 0:
            return 0
        ranges[range_offs] -= 1
        res = get_num_subst(syms, ranges, mem, syms_offs + 1, range_offs, True)
        ranges[range_offs] += 1
    elif c == '.':
        if range_offs < nr and ranges[range_offs] != 0 and cont:
            return 0
        if range_offs < nr and ranges[range_offs] == 0:
            res = get_num_subst(syms, ranges, mem, syms_offs + 1, range_offs + 1, False)
        else:
            res = get_num_subst(syms, ranges, mem, syms_offs + 1, range_offs, False)
    elif c == '?':
        syms[syms_offs] = '#'
        n1 = get_num_subst(syms, ranges, mem, syms_offs, range_offs, cont)
        syms[syms_offs] = '.'
        n2 = get_num_subst(syms, ranges, mem, syms_offs, range_offs, cont)
        syms[syms_offs] = '?'
        res = n1 + n2

    mem[key] = res
    return res

def expand(e, n=5):
    return list("?".join(["".join(e[0])] * n)), e[1] * n


entries = [parse_line(line) for line in lines]
res1 = sum(get_num_subst(s, r, {}) for s, r in entries)
print(f"Answer 1: {res1}")

entries_expanded = [expand(e, 5) for e in entries]
res2 = sum(get_num_subst(s, r, {}) for s, r in entries_expanded)
print(f"Answer 2: {res2}")
