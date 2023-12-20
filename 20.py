# DAY20
from collections import deque
import math
import functools

f = open('input/20.txt', 'r')
lines = [line.strip() for line in f.readlines()]

TYPE_NONE = 0
TYPE_FLIPFLOP = 1
TYPE_CONJ = 2

SIG_LOW = 0
SIG_HIGH = 1


def parse_line(line):
    parts = line.split('->')
    name = parts[0].strip()
    mtype = TYPE_NONE
    if name[0] == '%':
        mtype = TYPE_FLIPFLOP
    elif name[0] == '&':
        mtype = TYPE_CONJ
    if mtype != TYPE_NONE:
        name = name[1:]
    outputs = []
    if len(parts) > 1:
        outputs = [x.strip() for x in parts[1].split(', ') if x != '']
    return name, (mtype, outputs)


def get_inputs(mods):
    res = {}
    for mname, (_, outputs) in mods.items():
        for mout in outputs:
            if mout not in res:
                res[mout] = {}
            res[mout][mname] = SIG_LOW
    return res


def eval(mods, times=1, wait_for_sig=None, start_mod_name='broadcaster', start_sig_type=SIG_LOW):
    minputs = get_inputs(mods)
    mstate = {mname: [False, minputs[mname]] for mname in minputs.keys()}
    sig_counts = {SIG_LOW: 0, SIG_HIGH: 0}

    presses = 0
    while True:
        mq = deque()
        mq.append((start_mod_name, start_sig_type))
        while len(mq) > 0:
            mname, stype = mq.popleft()
            sig_counts[stype] += 1
            if mname == wait_for_sig and stype == SIG_LOW:
                return sig_counts, presses + 1
            if mname not in mods:
                continue
            mtype, outputs = mods[mname]
            out_stype = stype
            if mtype == TYPE_FLIPFLOP:
                if stype == SIG_LOW:
                    state = mstate[mname][0]
                    if state:
                        out_stype = SIG_LOW
                        mstate[mname][0] = False
                    else:
                        out_stype = SIG_HIGH
                        mstate[mname][0] = True
                else:
                    continue
            elif mtype == TYPE_CONJ:
                inputs = mstate[mname][1]
                if all(s == SIG_HIGH for s in inputs.values()):
                    out_stype = SIG_LOW
                else:
                    out_stype = SIG_HIGH

            for mout in outputs:
                mstate[mout][1][mname] = out_stype
                mq.append((mout, out_stype))
        presses += 1
        if times > 0 and presses == times:
            break
    return sig_counts, presses


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def lcm_arr(arr):
    return functools.reduce(lambda a, b: lcm(a, b), arr)


mods = {name: conf for name, conf in map(parse_line, lines)}
counts, _ = eval(mods, 10000)
cv = list(counts.values())
res1 = counts[0] * counts[1]
print(res1)

minputs = get_inputs(mods)
in1 = list(minputs['rx'].keys())[0]
in2 = minputs[in1].keys()
steps = []
for mname in in2:
    _, s = eval(mods, -1, mname)
    steps.append(s)
res2 = lcm_arr(steps)
print(res2)
