from functools import lru_cache
from util.files import read_file


def split(num):
    idx_half = len(num) // 2
    return (num[:idx_half].lstrip("0") or "0"), (num[idx_half:].lstrip("0") or "0")


def multiply(num):
    return str(int(num) * 2024)


@lru_cache(None)
def blink(num, times):
    if times == 0:
        return 1

    if num == "0":
        return blink("1", times - 1)

    if len(num) % 2 == 0:
        num_l, num_r = split(num)
        return blink(num_l, times - 1) + blink(num_r, times - 1)

    return blink(multiply(num), times - 1)


if __name__ == "__main__":
    input = read_file("day11/input.txt")[0]

    output = 0

    for i in input:
        output += blink(i, 75)

    print(f"Stones: {output}")
