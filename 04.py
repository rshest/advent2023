# DAY04
f = open('input/04.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_card(line):
    line = line.split(": ")[1]
    n1, n2 = line.split("|")
    player_nums = [int(x.strip()) for x in n2.strip().split()]
    winning_nums = [int(x.strip()) for x in n1.strip().split()]
    return (winning_nums, player_nums)

def get_num_matches(card):
    common = set(card[0]).intersection(set(card[1]))
    return len(common)

def get_score(card):
    num_matches = get_num_matches(card)
    return int(2 ** num_matches / 2)

def eval_num_copies(cards):
    ncards = len(cards)
    copies = [1] * ncards
    for i in range(ncards):
        nm = get_num_matches(cards[i])
        for j in range(i + 1, min(i + 1 + nm, ncards)):
            copies[j] += copies[i]
    return copies

cards = [parse_card(line) for line in lines]

res1 = sum(get_score(c) for c in cards)
print(res1)

copies = eval_num_copies(cards)
res2 = sum(copies)
print(res2)
