from util.files import read_file

seen = {}


def find_starts(grid):
    starts = []

    for idx_r, r in enumerate(grid):
        for idx_c, c in enumerate(r):
            if c == "0":
                starts.append((idx_r, idx_c))

    return starts


def follow_trail(grid, start):
    nodes = [start]

    while True:
        nexts = []

        for node in nodes:
            seen.setdefault(node, check_surrounding(grid, node))
            nexts += seen[node]

        nodes = list(set(nexts))

        if reached_peak(grid, nodes[0]):
            return len(nodes)

        if len(nodes) == 0:
            return 0


def follow_trail_2(grid, start):
    nodes = [start]

    while True:
        nexts = []

        for node in nodes:
            seen.setdefault(node, check_surrounding(grid, node))
            nexts += seen[node]

        nodes = list(nexts)

        if reached_peak(grid, nodes[0]):
            return len(nodes)

        if len(nodes) == 0:
            return 0


def reached_peak(grid, node):
    return grid[node[0]][node[1]] == "9"


def check_surrounding(grid, point):
    r, c = point
    value = int(grid[r][c])
    surrounding = []

    if 0 <= r - 1 < len(grid):
        surrounding += [(r - 1, c)] if grid[r - 1][c] == str(int(value + 1)) else []

    if 0 <= r + 1 < len(grid):
        surrounding += [(r + 1, c)] if grid[r + 1][c] == str(int(value + 1)) else []

    if 0 <= c - 1 < len(grid[0]):
        surrounding += [(r, c - 1)] if grid[r][c - 1] == str(int(value + 1)) else []

    if 0 <= c + 1 < len(grid[0]):
        surrounding += [(r, c + 1)] if grid[r][c + 1] == str(int(value + 1)) else []

    return surrounding


if __name__ == "__main__":
    input = read_file("day10/input.txt", sep="")

    starts = find_starts(input)
    scores = [follow_trail(input, start) for start in starts]

    print(f"Part 1: {sum(scores)}")

    scores = [follow_trail_2(input, start) for start in starts]

    print(f"Part 2: {sum(scores)}")
