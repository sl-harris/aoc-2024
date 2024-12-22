from functools import cache
from util.grid import step, INCREMENTS_DIR, DIRECTIONS
from util.files import read_file

NUMPAD = ["789", "456", "123", " 0A"]
DIRPAD = ["#^A", "<v>"]

START_NUMPAD = (3, 2)
START_DIRPAD = (0, 2)


def contains_blank(path, pad):
    for loc in path:
        r, c = loc

        if pad[r][c] == " ":
            return True

    return False


def solve(grid, start, end):
    queue = [(start, [], [start])]
    paths = []

    while True:
        if not queue:
            break

        start_, steps, seen = queue.pop(0)

        if start_ == end:
            paths.append(steps)
            continue

        for d in DIRECTIONS:
            loc = step(grid, start_, d)

            if loc and loc not in seen:
                queue.append((loc, steps + [d], seen + [loc]))

    return paths


def find(val, pad):
    for r, row in enumerate(pad):
        if row.count(val) > 0:
            return (r, row.index(val))


@cache
def solve_dirpad(start, end, level):
    if start == end:
        return 1

    paths = solve(DIRPAD, start, end)

    if level == 1:
        return min([len(s) + 1 for s in solve(DIRPAD, start, end)])

    costs = []

    for path in paths:
        cost = 0
        path = ["A"] + path + ["A"]

        for idx in range(len(path) - 1):
            cost += solve_dirpad(
                LOCS_DIRS[path[idx]], LOCS_DIRS[path[idx + 1]], level - 1
            )

        costs.append(cost)

    return min(costs)


def solve_pad_single(start, end, pad=NUMPAD):
    v_start = min(start[1], end[1])
    v_end = max(start[1], end[1])

    h_start = min(start[0], end[0])
    h_end = max(start[0], end[0])

    v_seq = range(v_start, v_end + 1)
    v_seq = reversed(v_seq) if start[1] > end[1] else v_seq
    v_seq = list(v_seq)

    h_seq = range(h_start, h_end + 1)
    h_seq = reversed(h_seq) if start[0] > end[0] else h_seq
    h_seq = list(h_seq)

    paths = []

    v_first = [(h, v_seq[0]) for h in h_seq]
    v_first += [(h_seq[-1], v) for v in v_seq[1:]] if len(v_seq) > 1 else []

    if not contains_blank(v_first, pad):
        paths.append(tuple(v_first))

    h_first = [(h_seq[0], v) for v in v_seq]
    h_first += [(h, v_seq[-1]) for h in h_seq[1:]] if len(h_seq) > 1 else []

    if not contains_blank(h_first, pad):
        paths.append(tuple(h_first))

    return list(set(paths))


def solve_pad(num, start, pad):
    num_ = pad[start[0]][start[1]] + num

    paths = []

    for idx in range(len(num_) - 1):
        start = find(num_[idx], pad)
        end = find(num_[idx + 1], pad)
        solved = solve_pad_single(start, end, pad)

        if paths:
            paths = [path + [solved_] for solved_ in solved for path in paths]
        else:
            paths = [[path] for path in solved]

    return paths


def convert_path_to_dir_single(start, end):
    inc_r = end[0] - start[0]
    inc_c = end[1] - start[1]
    return INCREMENTS_DIR[(inc_r, inc_c)]


def convert_path_to_dir(path):
    return [
        [convert_path_to_dir_single(p[idx], p[idx + 1]) for idx in range(len(p) - 1)]
        for p in path
    ]


def solve_seq(num, level):
    num_path = solve_pad(num, START_NUMPAD, NUMPAD)
    num_dirs = [convert_path_to_dir(p) for p in num_path]

    paths = [["".join(dir) for dir in dirs] for dirs in num_dirs]
    paths = ["A".join(d) + "A" for d in paths]

    costs = []

    for path in paths:
        path = "A" + path
        cost = 0

        for idx in range(len(path) - 1):
            cost += solve_dirpad(LOCS_DIRS[path[idx]], LOCS_DIRS[path[idx + 1]], level)

        costs.append(cost)

    return costs


input = read_file("day21/sample.txt", sep="")

DIRS = "^v<>A"
LOCS_DIRS = {d: find(d, DIRPAD) for d in DIRS}

NUMS = "0123456789A"
LOCS_NUMS = {n: find(n, NUMPAD) for n in NUMS}

complexity = 0

for num in input:
    complexity += min(solve_seq(num, 25)) * int(num.replace("A", ""))

print(complexity)
