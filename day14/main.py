from util.files import read_file
import math


# W, H = 11, 7
W, H = 101, 103


def parse_input(input):
    input_ = []

    for i in input:
        p_v = i.split(" v=")

        p = p_v[0].replace("p=", "").split(",")
        p = (
            int(p[1]),
            int(p[0]),
        )

        v = p_v[1].split(",")
        v = (
            int(v[1]),
            int(v[0]),
        )

        input_.append((p, v))

    return input_


def move(p, v, s):
    new_p_x = p[0] + s * v[0]
    new_p_y = p[1] + s * v[1]

    new_p_x = new_p_x % H
    new_p_y = new_p_y % W

    return (new_p_x, new_p_y)


def allocate_quarters(locs):
    bound_v, bound_h = W // 2, H // 2
    qs = [0, 0, 0, 0]

    for x, y in locs:
        if x == bound_h or y == bound_v:
            continue

        if x < bound_h and y < bound_v:
            qs[0] += 1
            continue

        if x < bound_h and y > bound_v:
            qs[1] += 1
            continue

        if y < bound_v:
            qs[2] += 1
            continue

        if y > bound_v:
            qs[3] += 1
            continue

    return qs


def no_duplicates(locs):
    return len(locs) == len(set(locs))


def find_easter_egg(input):
    total_s = 0

    ps = [i[0] for i in input]
    vs = [i[1] for i in input]

    while True:
        ps = [move(p, v, 1) for p, v in zip(ps, vs)]
        total_s += 1

        if no_duplicates(ps):
            return total_s, ps


def display(locs):
    grid = []

    for x in range(H):
        grid.append([])

        for y in range(W):
            grid[x].append("X" if (x, y) in locs else " ")

    for r in grid:
        print("".join(r))


if __name__ == "__main__":
    input = read_file("day14/input.txt", sep="")
    input = parse_input(input)

    s = 100

    new_locs = [move(p, v, s) for (p, v) in input]
    qs = allocate_quarters(new_locs)

    print(f"Part 1: {math.prod(qs)}")

    secs, locs = find_easter_egg(input)

    print(f"Part 2: {secs}")
    display(locs)
