from util.files import read_file

INCREMENTS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def assign_region_to_grid(grid):
    regions = copy_grid(grid)

    queue = [find_unassigned_region(regions)]
    curr_region = 0

    while queue:
        unassigned = queue.pop(0)
        curr_region, regions = assign_region_to_coord(
            grid, regions, unassigned, curr_region
        )

        if same_plants := find_near_same_plants(grid, regions, unassigned):
            queue = same_plants + queue
            continue

        if next_unassigned := find_unassigned_region(regions):
            queue += [next_unassigned] if next_unassigned not in queue else []

    return regions, curr_region


def copy_grid(grid):
    grid_ = [[] for _ in range(len(grid))]
    grid_ = [[-1] * len(grid[0]) for _ in grid_]
    return grid_


def find_unassigned_region(regions):
    for r, row in enumerate(regions):
        for c, col in enumerate(row):
            if col == -1:
                return (r, c)

    return False


def assign_region_to_coord(grid, regions, start, curr_region):
    r, c = start

    if region := find_equal_region(grid, regions, start):
        regions[r][c] = region
    else:
        regions[r][c] = (curr_region := curr_region + 1)

    return curr_region, regions


def find_equal_region(grid, regions, start):
    r, c = start
    plant = grid[r][c]

    if r - 1 >= 0 and grid[r - 1][c] == plant and regions[r - 1][c] > -1:
        return regions[r - 1][c]

    if r + 1 < len(grid) and grid[r + 1][c] == plant and regions[r + 1][c] > -1:
        return regions[r + 1][c]

    if c - 1 >= 0 and grid[r][c - 1] == plant and regions[r][c - 1] > -1:
        return regions[r][c - 1]

    if c + 1 < len(grid[0]) and grid[r][c + 1] == plant and regions[r][c + 1] > -1:
        return regions[r][c + 1]

    return False


def find_near_same_plants(grid, regions, coord):
    r, c = coord
    plant = grid[r][c]
    same_plants = []

    if r - 1 >= 0 and grid[r - 1][c] == plant and regions[r - 1][c] == -1:
        same_plants.append((r - 1, c))

    if r + 1 < len(grid) and grid[r + 1][c] == plant and regions[r + 1][c] == -1:
        same_plants.append((r + 1, c))

    if c - 1 >= 0 and grid[r][c - 1] == plant and regions[r][c - 1] == -1:
        same_plants.append((r, c - 1))

    if c + 1 < len(grid[0]) and grid[r][c + 1] == plant and regions[r][c + 1] == -1:
        same_plants.append((r, c + 1))

    return same_plants


def calc_perimeter(regions, region_num):
    perimeter = 0

    for r, row in enumerate(regions):
        for c, reg in enumerate(row):
            if reg != region_num:
                continue

            perimeter += 1 if r - 1 < 0 or regions[r - 1][c] != region_num else 0
            perimeter += (
                1 if r + 1 == len(regions) or regions[r + 1][c] != region_num else 0
            )
            perimeter += 1 if c - 1 < 0 or regions[r][c - 1] != region_num else 0
            perimeter += (
                1 if c + 1 == len(regions[0]) or regions[r][c + 1] != region_num else 0
            )

    return perimeter


def calc_area(regions, region_num):
    return sum([row.count(region_num) for row in regions])


def calc_num_sides(regions, region_num):
    corners = find_corners(regions, region_num)
    return len(corners)


def find_corners(regions, region_num):
    borders = []

    for r, row in enumerate(regions):
        for c, reg in enumerate(row):
            if reg != region_num:
                continue

            r_min_1 = r - 1 < 0 or regions[r - 1][c] != region_num
            r_pls_1 = r + 1 >= len(regions) or regions[r + 1][c] != region_num

            c_min_1 = c - 1 < 0 or regions[r][c - 1] != region_num
            c_pls_1 = c + 1 >= len(regions[0]) or regions[r][c + 1] != region_num

            diag_tl = (
                not (0 <= r - 1 < len(grid) and 0 <= c - 1 < len(grid[0]))
                or regions[r - 1][c - 1] != region_num
            )
            diag_tr = (
                not (0 <= r - 1 < len(grid) and 0 <= c + 1 < len(grid[0]))
                or regions[r - 1][c + 1] != region_num
            )

            diag_bl = (
                not (0 <= r + 1 < len(grid) and 0 <= c - 1 < len(grid[0]))
                or regions[r + 1][c - 1] != region_num
            )
            diag_br = (
                not (0 <= r + 1 < len(grid) and 0 <= c + 1 < len(grid[0]))
                or regions[r + 1][c + 1] != region_num
            )

            # TL corner
            if diag_tl and r_min_1 and c_min_1:
                borders += [f"H-{r}", f"V-{c}"]

            # TR corner
            if diag_tr and r_min_1 and c_pls_1:
                borders += [f"H-{r}", f"V-{c+1}"]

            # BL corner
            if diag_bl and r_pls_1 and c_min_1:
                borders += [f"H-{r+1}", f"V-{c}"]

            # BR corner
            if diag_br and r_pls_1 and c_pls_1:
                borders += [f"H-{r+1}", f"V-{c+1}"]

    borders = list(set(borders))
    return borders


def find_borders(regions, region_num):
    borders = []

    for r, row in enumerate(regions):
        for c, reg in enumerate(row):
            if reg != region_num:
                continue

            if r - 1 < 0 or regions[r - 1][c] != region_num:
                borders.append((r, c, "^"))

            if r + 1 == len(regions) or regions[r + 1][c] != region_num:
                borders.append((r, c, "v"))

            if c - 1 < 0 or regions[r][c - 1] != region_num:
                borders.append((r, c, "<"))

            if c + 1 == len(regions[0]) or regions[r][c + 1] != region_num:
                borders.append((r, c, ">"))

    return borders


def calc_num_sides(borders):
    borders_ = borders.copy()
    sides = []

    while borders_:
        r, c, dir = borders_.pop(0)

        if dir in ["^", "v"]:
            if borders.count((r, c + 1, dir)) > 0:
                continue

            if borders_.count((r, c - 1, dir)) > 0:
                borders_.insert(borders.index((r, c - 1, dir)), (r, c, dir))

        if dir in ["<", ">"]:
            if borders.count((r + 1, c, dir)) > 0:
                continue

            if borders_.count((r - 1, c, dir)) > 0:
                borders_.insert(borders.index((r - 1, c, dir)), (r, c, dir))

        sides.append((r, c, dir))

    return sides


if __name__ == "__main__":
    input = read_file("day12/input.txt", sep="")
    grid = [list(row) for row in input]
    regions, num_regions = assign_region_to_grid(grid)

    areas = [calc_area(regions, region) for region in range(1, num_regions + 1)]
    perimeters = [
        calc_perimeter(regions, region) for region in range(1, num_regions + 1)
    ]
    price = sum([area * perimeter for area, perimeter in zip(areas, perimeters)])
    print(f"Part 1: {price}")

    # sides = [calc_num_sides(regions, region) for region in range(1, num_regions + 1)]

    borders = [find_borders(regions, region) for region in range(1, num_regions + 1)]
    sides = [calc_num_sides(b) for b in borders]
    price = sum([area * len(side) for area, side in zip(areas, sides)])

    print(f"Part 2: {price}")
