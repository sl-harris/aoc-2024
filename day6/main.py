from util.files import read_file
from copy import deepcopy

NEXT_DIR = {"^": ">", ">": "v", "v": "<", "<": "^"}
INCREMENTS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def find_start(input):
    for idx_r, row in enumerate(input):
        for idx_c, col in enumerate(row):
            if col == "^":
                return idx_r, idx_c


def mark_x(input, start_r, start_c, dir):
    inc_r, inc_c = INCREMENTS[dir]

    while True:
        input[start_r][start_c] = "X"

        if (
            start_r + inc_r in [-1, len(input)]
            or start_c + inc_c in [-1, len(input)]
            or input[start_r + inc_r][start_c + inc_c] == "#"
        ):
            dir = NEXT_DIR[dir]
            break

        start_r += inc_r
        start_c += inc_c

    return start_r, start_c, dir


def find_exit(input, start_r, start_c):
    dir = input[start_r][start_c]

    while True:
        if start_r in [0, len(input) - 1] or start_c in [0, len(input) - 1]:
            break

        start_r, start_c, dir = mark_x(input, start_r, start_c, dir)

    return start_r, start_c


def count_x(input):
    return sum(["".join(r).count("X") for r in input])


def is_loop(input, start_r, start_c):
    dir = input[start_r][start_c]

    curr_r, curr_c = start_r, start_c
    path_taken = []

    while True:
        if (curr_r, curr_c, dir) in path_taken:
            break

        if curr_r in [0, len(input) - 1] or curr_c in [0, len(input) - 1]:
            return False

        path_taken.append((curr_r, curr_c, dir))
        curr_r, curr_c, dir = mark_x(input, curr_r, curr_c, dir)

    return True


def experiment_obstacle(input, start_r, start_c, obstacles):

    print(f"There are {len(obstacles)} obstacles.")

    obs_loop = []

    for idx, (obs_r, obs_c) in enumerate(obstacles):
        if (idx + 1) % 50 == 0:
            print(f"Experimenting obstacle #{idx+1}")

        input_ = deepcopy(input)
        input_[obs_r][obs_c] = "#"

        if is_loop(input_, start_r, start_c):
            obs_loop.append((obs_r, obs_c, input_))

    return obs_loop


def get_obstacles(input_p1, start_r, start_c):
    obs = []

    for idx_r, r in enumerate(input_p1):
        for idx_c, _ in enumerate(r):
            if input_p1[idx_r][idx_c] == "X":
                obs.append((idx_r, idx_c))

    if (start_r, start_c) in obs:
        obs.remove((start_r, start_c))

    return obs


if __name__ == "__main__":
    input = read_file("day6/input.txt")
    input = [list(r) for r in input]

    start_r, start_c = find_start(input)
    input_ = deepcopy(input)
    exit = find_exit(input_, start_r, start_c)

    obstacles = get_obstacles(input_, start_r, start_c)

    print(f"Part 1: {count_x(input_)}")

    input_ = deepcopy(input)

    obstacles = experiment_obstacle(input_, start_r, start_c, obstacles)
    print(f"Part 2: {len(obstacles)}")
