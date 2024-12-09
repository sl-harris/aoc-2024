from math import ceil
from util.files import read_file


def get_max_id(input):
    return int(len(input) / 2)


def get_front(input):
    return input[2:], int(input[0]), int(input[1])


def get_back(input):
    return input[:-2], int(input[-1]), int(input[-2]) if len(input) > 1 else -1


def append_file(file, size, id):
    return file + [id for _ in range(size)]


def build_file(input, max_id):
    file = []

    current_id = 0
    current_back_id = max_id
    file_size_back = 0

    while True:
        if len(input) < 2:
            break

        # Get the front two
        input, file_size_front, free_size = get_front(input)

        # Build file
        file = append_file(file, file_size_front, current_id)

        while True:
            if free_size < 1 or len(input) < 1:
                break

            # Fill the free space from the back, if there's none remaining
            if file_size_back < 1:
                input, file_size_back, _ = get_back(input)

            fill_size = min(file_size_back, free_size)

            # Fill free space
            file = append_file(file, fill_size, current_back_id)

            free_size -= fill_size
            file_size_back -= fill_size

            # Decrement ID
            if file_size_back < 1:
                current_back_id -= 1

        # Increment ID
        current_id += 1

    # Process last bits
    file_size_front = int(input[0]) if len(input) > 0 else 0

    file = append_file(file, file_size_front, current_id)
    file = append_file(file, file_size_back, current_back_id)

    return file


def find_file(file_system, file_idx):
    for idx, file in reversed(list(enumerate(file_system))):
        if file[0] == "File" and file[2] == file_idx:
            return idx


def find_free_space(file_system, size_required, file_idx):
    for idx, (file_type, file_size, _) in enumerate(file_system):
        if file_type == "File":
            continue

        if idx >= file_idx:
            return False

        if file_size >= size_required:
            return idx

    return False


def move_file(file_system, file_idx, free_space_idx):
    file = file_system[file_idx]
    free_space = file_system[free_space_idx]

    file_system[file_idx] = ("Free", file[1], 0)
    file_system[free_space_idx] = file

    free_space_remaining = free_space[1] - file[1]
    if free_space_remaining:
        file_system.insert(free_space_idx + 1, ("Free", free_space_remaining, 0))

    return file_system


def build_file_p2(input):
    file_system = []
    is_file = True
    idx = 0

    for i in input:
        if is_file:
            file_system.append(("File", int(i), idx))
            idx += 1

        if not is_file:
            file_system.append(("Free", int(i), 0))

        is_file = not is_file

    for i in reversed(range(idx)):
        idx = find_file(file_system, i)
        _, file_size, _ = file_system[idx]

        free_space_idx = find_free_space(file_system, file_size, idx)

        if free_space_idx:
            file_system = move_file(file_system, idx, free_space_idx)

    flattened = []

    for _, file_size, file_idx in file_system:
        for _ in range(file_size):
            flattened.append(file_idx)

    return flattened


def calc_checksum(input):
    return sum([idx * int(chr) for idx, chr in enumerate(input)])


if __name__ == "__main__":
    input = read_file("day9/input.txt", sep="")[0]
    file = build_file(input, get_max_id(input))
    checksum = calc_checksum(file)

    print(f"Part 1: {checksum}")

    input = read_file("day9/input.txt", sep="")[0]
    file_p2 = build_file_p2(input)
    checksum = calc_checksum(file_p2)
    print(f"Part 2: {checksum}")
