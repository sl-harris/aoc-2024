from util.files import read_file
from util.grid import INCREMENTS_DIR

NUMPAD = ["789", "456", "123", " 0A"]
DIRPAD = [" ^A", "<v>"]

START_NUMPAD = (3, 2)
START_DIRPAD = (0, 2)


def contains_blank(path, pad):
    for loc in path:
        r, c = loc

        if pad[r][c] == " ":
            return True

    return False


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

    v_first = [(h, v_seq[0]) for h in h_seq]
    v_first += [(h_seq[-1], v) for v in v_seq[1:]] if len(v_seq) > 1 else []

    h_first = [(h_seq[0], v) for v in v_seq]
    h_first += [(h, v_seq[-1]) for h in h_seq[1:]] if len(h_seq) > 1 else []

    return v_first if contains_blank(h_first, pad) else h_first


def convert_path_to_dir_single(start, end):
    inc_r = end[0] - start[0]
    inc_c = end[1] - start[1]
    return INCREMENTS_DIR[(inc_r, inc_c)]


def convert_path_to_dir(path):
    return [
        convert_path_to_dir_single(path[idx], path[idx + 1])
        for idx in range(len(path) - 1)
    ]


def find(val, pad):
    for r, row in enumerate(pad):
        if row.count(val) > 0:
            return (r, row.index(val))


def solve_pad(num, start, pad):
    num_ = pad[start[0]][start[1]] + num

    paths = []

    for idx in range(len(num_) - 1):
        start = find(num_[idx], pad)
        end = find(num_[idx + 1], pad)
        paths.append(solve_pad_single(start, end, pad))

    return paths


def solve_seqs(num, num_dir_layers):
    paths = [num]

    num_path = solve_pad(num, START_NUMPAD, NUMPAD)
    num_dirs = [convert_path_to_dir(p) for p in num_path]

    dir_dirs_str = ["".join(d) for d in num_dirs]
    dir_dirs_str = "A".join(dir_dirs_str) + "A"

    paths.append(dir_dirs_str)

    for _ in range(num_dir_layers):
        dir_path = solve_pad(dir_dirs_str, START_DIRPAD, DIRPAD)
        dir_dirs = [convert_path_to_dir(p) for p in dir_path]

        dir_dirs_str = ["".join(d) for d in dir_dirs]
        dir_dirs_str = "A".join(dir_dirs_str) + "A"

        paths.append(dir_dirs_str)

    return paths


def calc_complexity(nums, paths):
    return sum(
        [int(num.replace("A", "")) * len(path) for num, path in zip(nums, paths)]
    )


# 212830 TOO HIGH

input = read_file("day21/input.txt", sep="")
paths = [solve_seqs(num, 2)[-1] for num in input]

print(f"Part 1: {calc_complexity(input, paths)}")
