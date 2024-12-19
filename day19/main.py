from functools import lru_cache
from util.files import read_file


def parse_input(input):
    return input[0], input[1:]


@lru_cache(None)
def is_possible(design, towels, progress=""):
    if design == progress:
        return True

    if design[: len(progress)] != progress:
        return False

    for t in towels.split(", "):
        if is_possible(design, towels, progress + t):
            return True

    return False


@lru_cache(None)
def count_possible(design, towels, progress=""):
    if design == progress:
        return 1

    if design[: len(progress)] != progress:
        return 0

    return sum(
        [count_possible(design, towels, progress + t) for t in towels.split(", ")]
    )


if __name__ == "__main__":
    input = read_file("day19/input.txt", sep="")
    towels, designs = parse_input(input)

    possibles = [is_possible(d, towels) for d in designs]
    print(f"Part 1: {sum(possibles)}")

    counts = [count_possible(d, towels) for d in designs]
    print(f"Part 2: {sum(counts)}")
