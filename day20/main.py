from util.files import read_file
from util.grid import in_grid, DIRS, INCREMENTS


def parse_input(input):
    for r, row in enumerate(input):
        input[r] = list(row)

    for r, row in enumerate(input):
        for c, col in enumerate(row):
            if col == "S":
                return (r, c), input


def find_exit(grid, start):
    path = []

    while True:
        path.append(start)
        r, c = start
        val = grid[r][c]

        if val == "E":
            return path

        for d in DIRS:
            inc_r, inc_c = INCREMENTS[d]
            r_, c_ = r + inc_r, c + inc_c

            if (r_, c_) not in path and grid[r_][c_] in ".E":
                start = (r_, c_)
                break


def build_q_table(path):
    total = len(path)
    return {loc: total - idx - 1 for idx, loc in enumerate(path)}


def explore_cheat(grid, path, q_table):
    cheats = {}

    for p in path:
        r, c = p
        for d in DIRS:
            inc_r, inc_c = INCREMENTS[d]

            r_1, c_1 = r + inc_r, c + inc_c
            r_2, c_2 = r_1 + inc_r, c_1 + inc_c

            if (
                in_grid(grid, (r_2, c_2))
                and grid[r_1][c_1] == "#"
                and grid[r_2][c_2] in ".E"
                and q_table[(r_2, c_2)] < q_table[(r, c)]
            ):
                key = ((r, c), (r_2, c_2))
                cheats[key] = q_table[(r_2, c_2)] - q_table[(r, c)] + 2

    return cheats


def calc_distance(coord_1, coord_2):
    r_1, c_1 = coord_1
    r_2, c_2 = coord_2

    return abs(r_2 - r_1) + abs(c_2 - c_1)


def calc_savings(cheats, q_table):
    savings = {}

    for start, end in cheats:
        savings[(start, end)] = (
            q_table[start] - calc_distance(start, end) - q_table[end]
        )

    return savings


def calc_grid(loc):
    global grid, q_table
    r, c = loc

    coords = []

    if grid[r][c] not in "S.":
        return coords

    for r_ in range(r - 20, r + 21):
        for c_ in range(c - 20, c + 21):
            if not in_grid(grid, (r_, c_)):
                continue

            if not grid[r_][c_] in ".E":
                continue

            if calc_distance((r, c), (r_, c_)) <= 20:
                coords.append(((r, c), (r_, c_)))

    return coords


input = read_file("day20/input.txt", sep="")
start, grid = parse_input(input)

path = find_exit(grid, start)
q_table = build_q_table(path)
cheats = explore_cheat(grid, path, q_table)
cheats_100 = {key: value for key, value in cheats.items() if value <= -100}

print(f"Part 1: {len(cheats_100)}")

coords_ = []
for coord in q_table.keys():
    coords_ += calc_grid(coord)

savings = calc_savings(coords_, q_table)
savings_100 = {
    (start, end): value for (start, end), value in savings.items() if value >= 100
}

print(f"Part 2: {len(savings_100)}")
