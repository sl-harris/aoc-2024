from functools import lru_cache
from util.files import read_file
from util.grid import INCREMENTS, OTHER_DIRS, REVERSE
import math

REWARDS = {}
DIRS = "^v<>"


def parse_input(grid):
    start, end = None, None

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)

            if cell == "E":
                end = (r, c)

    return start, end


def find_empty_neighbour(coord, grid):
    neighbours = []

    for d in DIRS:
        inc_r, inc_c = INCREMENTS[d]
        r, c = coord[0] + inc_r, coord[1] + inc_c

        if grid[r][c] in [".", "S"]:
            neighbours.append((r, c, find_dir((r, c), coord)))

    return neighbours


def calc_delta(start, end):
    return end[0] - start[0], end[1] - start[1]


def find_dir(start, end):
    delta_r, delta_c = calc_delta(start, end)

    if delta_c == 1:
        return ">"

    if delta_c == -1:
        return "<"

    if delta_r == 1:
        return "v"

    if delta_r == -1:
        return "^"


def next_min_reward(coord, dir, rewards):
    r, c = coord
    inc_r, inc_c = INCREMENTS[dir]

    return min([rewards.get((r + inc_r, c + inc_c, d), math.inf) for d in DIRS])


def next_min_reward_(coord, dir, rewards):
    r, c = coord
    inc_r, inc_c = INCREMENTS[dir]

    return min(
        [
            rewards.get((r + inc_r, c + inc_c, d), math.inf)
            for d in DIRS
            if d != REVERSE[dir]
        ]
    )


def solve(end, grid):
    neighbours = find_empty_neighbour(end, grid)
    rewards = {n: 1 for n in neighbours}

    while True:
        neighbour = neighbours.pop(0)
        r, c, dir = neighbour
        reward = rewards[neighbour]

        neighbours_ = find_empty_neighbour((r, c), grid)
        neighbours_ = [
            (r_, c_, dir_) for r_, c_, dir_ in neighbours_ if dir_ != REVERSE[dir]
        ]

        for r_, c_, dir_ in neighbours_:
            reward_ = reward + 1 if dir_ == dir else reward + 1001

            rewards[(r_, c_, dir_)] = min(
                reward_, rewards.get((r_, c_, dir_), math.inf)
            )

            if reward_ <= rewards[(r_, c_, dir_)]:
                neighbours.append((r_, c_, dir_))

        if not neighbours:
            return rewards


def find_opt_paths(start, dir, budget):
    explore = [(*start, dir, budget)]
    paths = set([start])

    while True:
        if not explore:
            break

        r, c, dir, budget = explore.pop(0)

        for d in DIRS:
            inc_r, inc_c = INCREMENTS[d]
            r_, c_ = r + inc_r, c + inc_c
            next_budget = budget - (1 if dir == d else 1000)

            if next_min_reward_((r, c), d, rewards) <= budget:
                explore += [(r_, c_, d, next_budget)] if (r_, c_) not in paths else []
                paths.add((r_, c_))

    return paths


def find_opt_paths_(grid, start, budget, rewards):
    paths = []
    resolved = []

    paths.append((*start, ">", budget, [start]))

    while True:
        if not paths:
            break

        r, c, dir, b, current_path = paths.pop(0)

        for d in DIRS:
            if d == REVERSE[dir]:
                continue

            inc_r, inc_c = INCREMENTS[d]
            r_, c_ = r + inc_r, c + inc_c

            if grid[r_][c_] == "#":
                continue

            b_ = b - (1 if d == dir else 1001)

            if grid[r_][c_] == "E":
                resolved.append((current_path + [(r_, c_)], b_))
                continue

            if b_ <= 0:
                continue

            next_rewards = rewards.get((r_, c_), [])

            if (r_, c_) not in current_path and (
                b_ in next_rewards or (b_ - 1000) in next_rewards
            ):
                paths.append((r_, c_, d, b_, current_path + [(r_, c_)]))

    return resolved


def display_path(grid, path):
    h, w = len(grid), len(grid[0])

    for r in range(h):
        row = ""

        for c in range(w):
            if (r, c) in path:
                row += "O"
            else:
                row += input[r][c]

        print(row)


def build_s_table(rewards):
    rewards_ = {}

    for (r, c, dir), reward in rewards.items():
        rewards_.setdefault((r, c), [])
        rewards_[(r, c)].append(reward)

    return rewards_


if __name__ == "__main__":
    input = read_file("day16/input.txt", sep="")

    start, end = parse_input(input)
    grid = input

    rewards = solve(end, grid)
    rewards_ = {
        d: rewards.get((start[0], start[1], d), math.inf) + (1000 if d != ">" else 0)
        for d in DIRS
    }
    min_reward = min(rewards_.values())

    print(f"Part 1: {min_reward}")

    opt = find_opt_paths_(grid, start, min_reward, build_s_table(rewards))
    unique_nodes = set([node for path, _ in opt for node in path])

    print(f"Part 2: {len(unique_nodes)}")
