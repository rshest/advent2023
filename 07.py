# DAY07
from functools import cmp_to_key

f = open('input/07.txt', 'r')
lines = [line.strip() for line in f.readlines()]


def parse_card(line):
    p = line.split()
    return (p[0], int(p[1]))


def get_hist(card):
    res = {}
    for c in card:
        if c in res:
            res[c] += 1
        else:
            res[c] = 1
    return res


def get_hand_id_raw(card):
    h = get_hist(card)
    f = sorted(h.values(), reverse=True)
    if f[0] == 5:
        return 0
    elif f[0] == 4:
        return 1
    elif f[0] == 3 and f[1] == 2:
        return 2
    elif f[0] == 3:
        return 3
    elif f[0] == 2 and f[1] == 2:
        return 4
    elif f[0] == 2:
        return 5
    elif len(f) == 5:
        return 6
    else:
        return 7


def get_hand_id(card, use_joker=False):
    if not use_joker:
        return get_hand_id_raw(card)
    return min(get_hand_id_raw(card.replace('J', c)) for c in get_hist(card).keys())


def compare_cards(ca,  cb, ranks_map, use_joker=False):
    a, _ = ca
    b, _ = cb
    h1 = get_hand_id(a, use_joker)
    h2 = get_hand_id(b, use_joker)
    if h1 < h2:
        return -1
    elif h1 > h2:
        return 1
    for i in range(len(a)):
        r1 = ranks_map[a[i]]
        r2 = ranks_map[b[i]]
        if r1 < r2:
            return -1
        elif r1 > r2:
            return 1
    return 0


RANKS = "AKQJT98765432"
RANKS_MAP = {RANKS[i]: i for i in range(len(RANKS))}


def compare_cards1(ca, cb):
    return compare_cards(ca, cb, RANKS_MAP, False)


RANKS2 = "AKQT98765432J"
RANKS_MAP2 = {RANKS2[i]: i for i in range(len(RANKS2))}


def compare_cards2(ca, cb):
    return compare_cards(ca, cb, RANKS_MAP2, True)


def get_score(cards):
    return sum(cards[i][1] * (i + 1) for i in range(len(cards)))


cards = [parse_card(line) for line in lines]

cards = sorted(cards, key=cmp_to_key(compare_cards1), reverse=True)
res1 = get_score(cards)
print(res1)

cards = sorted(cards, key=cmp_to_key(compare_cards2), reverse=True)
res2 = get_score(cards)
print(res2)
