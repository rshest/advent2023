# DAY15
import re
data = open('input/15.txt', 'r').read()


def compute_hash(s):
    res = 0
    for c in s:
        res = (res + ord(c)) * 17 % 256
    return res


def parse_cmd(part):
    p = re.split(r'-|=', part)
    if p[1] == '':
        return (p[0], None)
    else:
        return (p[0], int(p[1]))


def eval_cmds(cmds):
    boxes = [([], {}) for i in range(256)]
    for label, n in cmds:
        id = compute_hash(label)
        lst, reg = boxes[id]
        if label not in reg:
            reg[label] = len(lst)
            lst.append((label, n))
        lst[reg[label]] = (label, n)
        if n is None:
            del reg[label]
    return boxes


def compute_score(boxes):
    res = 0
    for i in range(len(boxes)):
        lst, reg = boxes[i]
        offs = 0
        for j in range(len(lst)):
            _, n = lst[j]
            if n is None:
                offs += 1
            else:
                res += (i + 1) * (j + 1 - offs) * n
    return res


parts = data.strip().split(',')
res1 = sum(compute_hash(s) for s in parts)
print(res1)

cmds = [parse_cmd(p) for p in parts]
boxes = eval_cmds(cmds)
res2 = compute_score(boxes)
print(res2)
