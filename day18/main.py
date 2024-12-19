from util.files import read_file
from util.grid import step

REWARDS = {}
DIRS = "^v<>"


def parse_input(input, size, bytes):
    grid = [["."] * (size + 1) for _ in range(size + 1)]

    for i in range(bytes):
        c, r = input[i]
        grid[int(r)][int(c)] = "#"

    grid[0][0] = "S"
    grid[-1][-1] = "E"

    return grid


def solve(grid, start, end):
    seen = set(start)

    queue = [(start, 0)]

    while True:
        if not queue:
            break

        start_, steps = queue.pop(0)

        if start_ == end:
            return steps

        for d in DIRS:
            loc = step(grid, start_, d)

            if loc and loc not in seen:
                seen.add(loc)
                queue.append((loc, steps + 1))

    return False


if __name__ == "__main__":
    # size = 6
    # bytes = 12

    # input = read_file("day18/sample.txt", sep=",")

    size = 70
    bytes = 1024

    input = read_file("day18/input.txt", sep=",")

    global grid
    grid = parse_input(input, size, bytes)
    # print_grid(grid)

    score = solve(grid, (0, 0), (size, size))
    print(f"Part 1: {score}")

    for i in range(bytes, len(input)):
        c, r = input[i]
        grid[int(r)][int(c)] = "#"

        if not solve(grid, (0, 0), (size, size)):
            print(f"Part 2: ({c},{r})")
            break
