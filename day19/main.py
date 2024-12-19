from functools import lru_cache
from util.files import read_file


def parse_input(input):
    return input[0], input[1:]


@lru_cache(None)
def is_possible(design, towels):
    if design == "":
        return True

    for t in towels.split(", "):
        if design.startswith(t) and is_possible(design[len(t) :], towels):
            return True

    return False


@lru_cache(None)
def count_possible(design, towels):
    if design == "":
        return 1

    return sum(
        [
            count_possible(design[len(t) :], towels)
            for t in towels.split(", ")
            if design.startswith(t)
        ]
    )


if __name__ == "__main__":
    input = read_file("day19/input.txt", sep="")
    towels, designs = parse_input(input)

    possibles = [is_possible(d, towels) for d in designs]
    print(f"Part 1: {sum(possibles)}")

    counts = [count_possible(d, towels) for d in designs]
    print(f"Part 2: {sum(counts)}")
