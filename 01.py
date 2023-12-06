# DAY01
f = open('input/01.txt', 'r')
lines = [line.strip() for line in f.readlines()]

MAPPING = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def get_digit(s, dir=1, count_words=False):
    p = 0 if dir == 1 else len(s) - 1
    while p >= 0 and p < len(s):
        if s[p].isdigit():
            return s[p]
        if count_words:
            for k, v in MAPPING.items():
                if s[p:].startswith(k):
                    return str(v)
        p += dir

def get_number(line, count_words=False):
    n = int(get_digit(line, 1, count_words)) * 10 + int(get_digit(line, -1, count_words))
    return n

res1 = sum(get_number(l) for l in lines)
res2 = sum(get_number(l, True) for l in lines)

print(res1, res2)
