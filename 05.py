# DAY05
text = open('input/05.txt', 'r').read()

def parse_ints(line):
    return [int(x) for x in line.split()]

def parse_mapping(text):
    parts = text.split('\n')
    return [parse_ints(p) for p in parts[1:] if p != '']

def parse_problem(text):
    parts = text.split('\n\n')
    seeds = parse_ints(parts[0].split(': ')[1])
    mappings = [parse_mapping(p) for p in parts[1:]]
    return seeds, mappings

def map_seed(seed, mappings):
    for m in mappings:
        for d, s, l in m:
            if seed >= s and seed < s + l:
                seed = d + seed - s
                break
    return seed

def map_range(range, mapping):
    ranges = set()
    ranges.add(range)
    res = []
    while len(ranges) > 0:
        r = ranges.pop()
        ranges.add(r)
        mapped = False
        for d, s, l in mapping:
            rs, rl = r
            if (s < rs + rl) and (s + l > rs):
                p1 = d + max(s, rs) - s
                p2 = d + min(s + l, rs + rl) - s
                res.append((p1, p2 - p1))
                mapped = True
                # clip the range:
                ranges.remove(r)
                if rs < s:
                    ranges.add((rs, s - rs))
                if rs + rl > s + l:
                    ranges.add((s + l, rs + rl - s - l))
                break
        if not mapped:
            break
    res += list(ranges)
    return res

def map_ranges(ranges, mappings):
    for mapping in mappings:
        res = []
        for r in ranges:
            res += map_range(r, mapping)
            ranges = res
    return ranges

seeds, mappings = parse_problem(text)

res1 = min(map_seed(s, mappings) for s in seeds)
print(res1)

ranges = [(seeds[i * 2], seeds[i * 2 + 1]) for i in range(int(len(seeds)/2))]
res2 = min(x for x, _ in map_ranges(ranges, mappings))
print(res2)
