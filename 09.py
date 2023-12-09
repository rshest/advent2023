# DAY09

f = open('input/09.txt', 'r')


def parse_ints(line):
    return [int(x.strip()) for x in line.split()]


def get_derivatives(nums):
    n = len(nums)
    res = [0] * (n - 1)
    for i in range(n - 1):
        res[i] = nums[i + 1] - nums[i]
    return res


def extrapolate(nums):
    derivatives = [nums]
    n = nums
    while True:
        d = get_derivatives(n)
        if all(x == 0 for x in d):
            res1, res2 = 0, 0
            nd = len(derivatives)
            for i in range(nd):
                res1 = derivatives[nd - 1 - i][0] - res1
                res2 += derivatives[nd - 1 - i][-1]
            return res1, res2
        derivatives.append(d)
        n = d

nums = [parse_ints(line.strip()) for line in f.readlines()]

extr = [extrapolate(n) for n in nums]
res1 = sum(b for _, b in extr)
print(res1)

res2 = sum(a for a, _ in extr)
print(res2)
