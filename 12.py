f = open('input/12_test.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_line(line):
    parts = line.split()
    return list(parts[0]), [int(x.strip()) for x in parts[1].strip().split(",")]

mem = {}

def get_num_subst(syms, ranges, syms_offs=0, range_offs=0, cont=False):
    global mem
    nr = len(ranges)
    if syms_offs == len(syms) and (range_offs == nr or
                                   (range_offs == nr - 1 and ranges[range_offs] == 0)):
        return 1
    if syms_offs == len(syms):
        return 0
    c = syms[syms_offs]

    key = "".join(syms[syms_offs:]) + "|" + ",".join(
        str(x) for x in ranges[range_offs:]) + ("~" if cont else "")
    if key in mem:
        return mem[key]

    if c == '#':
        if range_offs == nr or ranges[range_offs] == 0:
            return 0
        ranges[range_offs] -= 1
        n = get_num_subst(syms, ranges, syms_offs + 1, range_offs, True)
        ranges[range_offs] += 1
        mem[key] = n
        return n
    elif c == '.':
        if range_offs < nr and ranges[range_offs] != 0 and cont:
            return 0
        if range_offs < nr and ranges[range_offs] == 0:
            n = get_num_subst(syms, ranges, syms_offs + 1, range_offs + 1, False)
        else:
            n = get_num_subst(syms, ranges, syms_offs + 1, range_offs, False)
        mem[key] = n
        return n
    elif c == '?':
        syms[syms_offs] = '#'
        n1 = get_num_subst(syms, ranges, syms_offs, range_offs, cont)
        syms[syms_offs] = '.'
        n2 = get_num_subst(syms, ranges, syms_offs, range_offs, cont)
        syms[syms_offs] = '?'
        mem[key] = n1 + n2
        return n1 + n2

def get_num_subst1(sym_ranges, ranges, sym_ranges_offs=0, ranges_offs=0):
    if sym_ranges_offs == len(sym_ranges):
        return int(ranges_offs == len(ranges))
    syms = sym_ranges[sym_ranges_offs]
    res = 0
    n = 0
    while ranges_offs + n <= len(ranges):
        ns = get_num_subst(syms, ranges[ranges_offs:ranges_offs + n])
        nsrest = 0
        if ns > 0:
            nsrest = get_num_subst1(sym_ranges, ranges, sym_ranges_offs + 1, ranges_offs + n)
        res += ns * nsrest
        n += 1
    return res


def expand(e, n=5):
    return list("?".join(["".join(e[0])] * n)), e[1] * n


def split_sym_ranges(e):
    rs = [list(p) for p in "".join(e).split('.')]
    return [r for r in rs if len(r) > 0]


entries = [parse_line(line) for line in lines]

nsubst = [get_num_subst(syms, ranges) for syms, ranges in entries]
res1 = sum(nsubst)
print(f"Answer 1: {res1}")

exp = [expand(e, 5) for e in entries]
nsubst2 = []

for i in range(len(exp)):
    syms, ranges = exp[i]
    syms_str = "".join(syms)
    print(f"{i + 1: >3}/{len(exp)}: {syms_str} | {ranges} ")
    n = get_num_subst1(split_sym_ranges(syms), ranges)
    nsubst2.append(n)

res2 = sum(nsubst2)
print(f"Answer 2: {res2}")
