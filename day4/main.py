from util.files import read_file


def find_xmas(input):
    return sum([line.count("XMAS") for line in input])


def count_horizontal(input):
    # Horizontal
    count = find_xmas(input)

    # Horizontal Rev
    input_rev = [line[::-1] for line in input]
    count += find_xmas(input_rev)

    return count


def count_vertical(input):
    # Vertical
    input_ver = [
        "".join(input[r][c] for r in range(len(input))) for c in range(len(input))
    ]
    count = find_xmas(input_ver)

    # Vertical Rev
    input_ver_rev = [line[::-1] for line in input_ver]
    count += find_xmas(input_ver_rev)

    return count


def count_diag_lr(input):
    # Diag LR
    input_diag_lr = []

    for c in reversed(range(len(input))):
        diag_line = ""

        for i in range(len(input) - c):
            diag_line += input[i][c + i]

        input_diag_lr.append(diag_line)

    for r in range(1, len(input)):
        diag_line = ""

        for i in range(len(input) - r):
            diag_line += input[r + i][i]

        input_diag_lr.append(diag_line)

    count = find_xmas(input_diag_lr)

    input_diag_lr_rev = [line[::-1] for line in input_diag_lr]
    count += find_xmas(input_diag_lr_rev)

    return count


def count_diag_rl(input):
    input_diag_rl = []

    for c in range(len(input)):
        diag_line = ""

        for i in range(c + 1):
            diag_line += input[i][c - i]

        input_diag_rl.append(diag_line)

    for r in range(1, len(input)):
        diag_line = ""

        for i in range(len(input) - r):
            diag_line += input[r + i][len(input) - i - 1]

        input_diag_rl.append(diag_line)

    count = find_xmas(input_diag_rl)

    # Diag RL Rev
    input_diag_rl_rev = [line[::-1] for line in input_diag_rl]
    count += find_xmas(input_diag_rl_rev)

    return count


def find_mas_diag_lr(input):
    # Diag LR
    input_diag_lr = []
    coord = []

    for c in reversed(range(len(input))):
        diag_line = ""

        for i in range(len(input) - c):
            diag_line += input[i][c + i]

        input_diag_lr.append(diag_line)
        coord.append((0, c))

    for r in range(1, len(input)):
        diag_line = ""

        for i in range(len(input) - r):
            diag_line += input[r + i][i]

        input_diag_lr.append(diag_line)
        coord.append((r, 0))

    mas_coords = find_mas_rl(input_diag_lr, coord)

    input_diag_lr_rev = [line[::-1] for line in input_diag_lr]
    mas_coords += find_mas_rl(input_diag_lr_rev, coord, is_rev=True)

    return mas_coords


def find_mas_rl(input, coord, is_rev=False):
    mas_centre = []

    for line, (start_x, start_y) in zip(input, coord):
        last_found = -1

        for _ in range(line.count("MAS")):
            last_found = line.find("MAS", last_found + 1)

            if not is_rev:
                mas_centre.append((start_x + last_found + 1, start_y + last_found + 1))
            else:
                mas_centre.append(
                    (
                        start_x + len(line) - last_found - 2,
                        start_y + len(line) - last_found - 2,
                    )
                )

    return mas_centre


def find_mas_diag_rl(input):
    input_diag_rl = []
    coord = []

    for c in range(len(input)):
        diag_line = ""

        for i in range(c + 1):
            diag_line += input[i][c - i]

        input_diag_rl.append(diag_line)
        coord.append((0, i))

    for r in range(1, len(input)):
        diag_line = ""

        for i in range(len(input) - r):
            diag_line += input[r + i][len(input) - i - 1]

        input_diag_rl.append(diag_line)
        coord.append((len(input) - i - 1, r + i))

    mas_coords = find_mas_lr(input_diag_rl, coord)

    # Diag RL Rev
    input_diag_rl_rev = [line[::-1] for line in input_diag_rl]
    mas_coords += find_mas_lr(input_diag_rl_rev, coord, is_rev=True)

    return mas_coords


def find_mas_lr(input, coord, is_rev=False):
    mas_centre = []

    for line, (start_x, start_y) in zip(input, coord):
        last_found = -1

        for _ in range(line.count("MAS")):
            last_found = line.find("MAS", last_found + 1)
            if not is_rev:
                mas_centre.append((start_x + last_found + 1, start_y - last_found - 1))
            else:
                mas_centre.append(
                    (
                        start_x + len(line) - last_found - 2,
                        start_y - len(line) + last_found + 2,
                    )
                )

    return mas_centre


if __name__ == "__main__":
    input = read_file("day4/input.txt", sep="")

    count_xmas = (
        count_horizontal(input)
        + count_vertical(input)
        + count_diag_rl(input)
        + count_diag_lr(input)
    )

    print(f"Part 1: {count_xmas}")

    mas_lr = find_mas_diag_lr(input)
    mas_rl = find_mas_diag_rl(input)
    intersect = list(set(mas_lr) & set(mas_rl))
    print(f"Part 2: {len(intersect)}")
