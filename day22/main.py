from util.files import read_file


def calc_secret_number_single(num):
    secret_num = num * 64
    secret_num ^= num
    secret_num %= 16777216

    secret_num_ = secret_num // 32
    secret_num ^= secret_num_
    secret_num %= 16777216

    secret_num_ = secret_num * 2048
    secret_num ^= secret_num_
    secret_num %= 16777216

    return secret_num


def calc_secret_number(num, times):
    secret_nums = [num]

    for _ in range(times):
        secret_nums.append(calc_secret_number_single(secret_nums[-1]))

    return secret_nums


def get_prices(output):
    return [[int(str(secret)[-1]) for secret in o] for o in output]


def get_deltas(prices):
    return [[end - start for end, start in zip(p[1:], p[:-1])] for p in prices]


def get_unique_deltas(deltas):
    uniques = set()

    for delta in deltas:
        for i in range(len(delta) - 4):
            uniques.add((delta[i], delta[i + 1], delta[i + 2], delta[i + 3]))

    return uniques


def find_price(prices, deltas, seq):
    combos = []

    for price, delta in zip(prices, deltas):
        delta = [0] + delta
        delta_ = [
            (delta[i], delta[i + 1], delta[i + 2], delta[i + 3])
            for i in range(len(delta) - 4)
        ]

        if delta_.count(seq) < 1:
            combos.append(0)
            continue

        idx = delta_.index(seq)
        combos.append(price[idx + 3])

    return combos


# {(-2, 2, -1, -1): 30}


def find_largest(prices, deltas):
    seqs = {}

    for price, delta in zip(prices, deltas):
        diffs = []
        price.pop(0)
        seen = set()

        while True:
            if not delta or not price:
                break

            diffs.append(delta.pop(0))
            price_ = price.pop(0)

            if len(diffs) < 4:
                continue

            seqs.setdefault(tuple(diffs), 0)

            if tuple(diffs) not in seen:
                seqs[tuple(diffs)] += price_
                seen.add(tuple(diffs))

            diffs = diffs[1:]

    return max(seqs.values())


input = read_file("day22/input.txt", sep="")
output = [calc_secret_number(int(i), 2000) for i in input]

output_p1 = [o[-1] for o in output]
print(f"Part 1: {sum(output_p1)}")

prices = get_prices(output)
deltas = get_deltas(prices)

print(f"Part 2: {find_largest(prices, deltas)}")
