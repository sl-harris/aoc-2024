from util.files import read_file


def measure_height(tool):
    columns = [0] * len(tool[0])

    for row in tool[1:-1]:
        for idx, char in enumerate(list(row)):
            columns[idx] += 1 if char == "#" else 0

    return tuple(columns)


def parse_input(input):
    locks, keys = [], []

    for idx in range(len(input) // 7):
        input_ = input[idx * 7 : idx * 7 + 7]

        if input_[0].count("#") == 5:
            locks.append(input_)

        if input_[0].count(".") == 5:
            keys.append(input_)

    return locks, keys


def can_fit(lock, key):
    for l, k in zip(lock, key):
        if l + k > 5:
            return False

    return True


input = read_file("day25/input.txt", sep="", include_blank=True)
locks, keys = parse_input(input)

locks = [measure_height(lock) for lock in locks]
keys = [measure_height(key) for key in keys]

can_fit = sum([can_fit(lock, key) for lock in locks for key in keys])

print(f"Part 1: {can_fit}")
