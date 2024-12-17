from util.files import read_file
from util.grid import INCREMENTS
import copy


def parse_input(input):
    for idx in range(1, len(input)):
        if all([val == "#" for val in input[idx]]):
            last_idx = idx

    grid = [list(r) for r in input[: last_idx + 1]]
    moves = "".join(input[last_idx + 1 :])

    return grid, moves


def print_grid(grid):
    for r in grid:
        print("".join(r))


def push(grid, loc, dir):
    r, c = loc
    inc_r, inc_c = INCREMENTS[dir]
    r_, c_ = r + inc_r, c + inc_c

    if grid[r_][c_] == ".":
        grid[r_][c_] = grid[r][c]
        grid[r][c] = "."
        return True

    if grid[r_][c_] == "O":
        if result := push(grid, (r_, c_), dir):
            grid[r_][c_] = grid[r][c]
            grid[r][c] = "."

            return True

    return False


def calc_score(grid):
    score = 0

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == "O":
                score += 100 * r + c

    return score


def parse_input_2(input):
    for idx in range(1, len(input)):
        if all([val == "#" for val in input[idx]]):
            last_idx = idx

    grid = [
        list(
            r.replace("#", "##")
            .replace(".", "..")
            .replace("O", "[]")
            .replace("@", "@.")
        )
        for r in input[: last_idx + 1]
    ]
    moves = "".join(input[last_idx + 1 :])

    return grid, moves


def is_box(grid, loc):
    r, c = loc

    if grid[r][c] == "[":
        return loc, (r, c + 1)

    if grid[r][c] == "]":
        return (r, c - 1), loc

    return False


def push_box(grid, loc_l, loc_r, dir):
    inc_r, inc_c = INCREMENTS[dir]

    r_l, c_l = loc_l
    r_l_, c_l_ = r_l + inc_r, c_l + inc_c

    r_r, c_r = loc_r
    r_r_, c_r_ = r_r + inc_r, c_r + inc_c

    if dir == "<":
        if grid[r_l_][c_l_] == "#":
            return False

        if grid[r_l_][c_l_] == "." or push_box(grid, *is_box(grid, (r_l_, c_l_)), dir):
            grid[r_l_][c_l_] = "["
            grid[r_l][c_l] = "]"
            grid[r_r][c_r] = "."
            return True

        return False

    if dir == ">":
        if grid[r_r_][c_r_] == "#":
            return False

        if grid[r_r_][c_r_] == "." or push_box(grid, *is_box(grid, (r_r_, c_r_)), dir):
            grid[r_r_][c_r_] = "]"
            grid[r_r][c_r] = "["
            grid[r_l][c_l] = "."
            return True

        return False

    if dir in "^v":
        if grid[r_r_][c_r_] == "#" or grid[r_l_][c_l_] == "#":
            return False

        if grid[r_r_][c_r_] == "." and grid[r_l_][c_l_] == ".":
            grid[r_r_][c_r_] = grid[r_r][c_r]
            grid[r_r][c_r] = "."
            grid[r_l_][c_l_] = grid[r_l][c_l]
            grid[r_l][c_l] = "."

            return True

        grid_ = copy.deepcopy(grid)

        box_1 = is_box(grid_, (r_l_, c_l_))
        box_1 = (not box_1) or push_box(grid_, *box_1, dir)

        box_2 = is_box(grid_, (r_r_, c_r_))
        box_2 = (not box_2) or push_box(grid_, *box_2, dir)

        if box_1 and box_2:
            copy_grid(grid_, grid)

            grid[r_l_][c_l_] = grid[r_l][c_l]
            grid[r_l][c_l] = "."

            grid[r_r_][c_r_] = grid[r_r][c_r]
            grid[r_r][c_r] = "."

            return True

        return False


def copy_grid(from_, to_):
    for idx_r, row in enumerate(from_):
        for idx_c, col in enumerate(row):
            to_[idx_r][idx_c] = col


def push_2(grid, loc, dir):
    r, c = loc
    inc_r, inc_c = INCREMENTS[dir]
    r_, c_ = r + inc_r, c + inc_c

    if grid[r_][c_] == ".":
        grid[r_][c_] = grid[r][c]
        grid[r][c] = "."
        return True

    if box := is_box(grid, (r_, c_)):
        box_l, box_r = box

        if push_box(grid, box_l, box_r, dir):
            grid[r_][c_] = grid[r][c]
            grid[r][c] = "."

            return True

    return False


def find_start(grid):
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == "@":
                return (r, c)


def calc_score_2(grid):
    score = 0

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col in "[":
                score += 100 * r + c
    return score


input = read_file("day15/input.txt", sep="")
grid, moves = parse_input(input)

r, c = find_start(grid)

print_grid(grid)

for m in moves:
    if push(grid, (r, c), m):
        inc_r, inc_c = INCREMENTS[m]
        r, c = r + inc_r, c + inc_c

print(f"Part 1: {calc_score(grid)}")

grid, moves = parse_input_2(input)
r, c = find_start(grid)

for m in moves:
    if push_2(grid, (r, c), m):
        inc_r, inc_c = INCREMENTS[m]
        r, c = r + inc_r, c + inc_c

print_grid(grid)
print(f"Part 2: {calc_score_2(grid)}")
