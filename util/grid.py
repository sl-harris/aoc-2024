INCREMENTS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
OTHER_DIRS = {"^": "^<>", "v": "v<>", "<": "^v<", ">": "^v>", "": "^v<>"}
REVERSE = {"^": "v", "v": "^", "<": ">", ">": "<"}
DIRS = "^v<>"


def print_grid(grid):
    for r in grid:
        print("".join(r))


def step(grid, loc, dir):
    r, c = loc
    inc_r, inc_c = INCREMENTS[dir]
    r_, c_ = r + inc_r, c + inc_c

    if r_ < 0 or r_ >= len(grid):
        return False

    if c_ < 0 or c_ >= len(grid):
        return False

    if grid[r_][c_] == "#":
        return False

    return (r_, c_)


def in_grid(grid, loc):
    return (0 <= loc[0] < len(grid)) and (0 <= loc[1] < len(grid[0]))
