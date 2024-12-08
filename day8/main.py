from itertools import combinations
from util.files import read_file


def find_antennas(input):
    antennas = {}

    for idx_r, r in enumerate(input):
        for idx_c, c in enumerate(r):
            if c != ".":
                antennas.setdefault(c, [])
                antennas[c].append((idx_r, idx_c))

    return antennas


def find_combos(antennas):
    combos = {}
    for key, value in antennas.items():
        combos[key] = list(combinations(value, 2))

    return combos


def find_distances(antennas):
    distances = {}

    for key, value in antennas.items():
        distances.setdefault(key, [])

        for (start_x, start_y), (end_x, end_y) in value:
            distances[key].append(((end_x - start_x), (end_y - start_y)))

    return distances


def find_antinode(combos, distances, grid):
    antinodes = {}

    for key in combos.keys():
        antinodes.setdefault(key, [])
        for ((start_x, start_y), (end_x, end_y)), (dist_x, dist_y) in zip(
            combos[key], distances[key]
        ):
            antinode_1 = (start_x - dist_x, start_y - dist_y)
            if is_valid_coord(antinode_1, grid):
                antinodes[key].append(antinode_1)

            antinode_2 = (end_x + dist_x, end_y + dist_y)
            if is_valid_coord(antinode_2, grid):
                antinodes[key].append(antinode_2)

    return antinodes


def find_resonant(combos, distances, grid):
    antinodes = {}

    for key in combos.keys():
        antinodes.setdefault(key, [])
        for ((start_x, start_y), (end_x, end_y)), (dist_x, dist_y) in zip(
            combos[key], distances[key]
        ):
            antinodes[key] += find_resonant_until_border(
                start_x, start_y, -dist_x, -dist_y, grid
            )
            antinodes[key] += find_resonant_until_border(
                end_x, end_y, dist_x, dist_y, grid
            )

    return antinodes


def find_resonant_until_border(coord_x, coord_y, dist_x, dist_y, grid):
    resonants = []

    while True:
        coord_x += dist_x
        coord_y += dist_y

        if not is_valid_coord((coord_x, coord_y), grid):
            break

        resonants.append((coord_x, coord_y))

    return resonants


def is_valid_coord(coord, grid):
    return (0 <= coord[0] < len(grid)) and (0 <= coord[1] < len(grid[0]))


if __name__ == "__main__":
    input = read_file("day8/input.txt", sep="")

    antennas = find_antennas(input)
    combos = find_combos(antennas)
    distances = find_distances(combos)
    antinodes = find_antinode(combos, distances, input)
    unique = list(
        set([antinode for antinodes_ in antinodes.values() for antinode in antinodes_])
    )

    print(f"Part 1: {len(unique)}")

    resonants = find_resonant(combos, distances, input)
    unique = list(
        set(
            [antinode for antinodes_ in resonants.values() for antinode in antinodes_]
            + [antenna_ for antenna in antennas.values() for antenna_ in antenna]
        )
    )

    print(f"Part 2: {len(unique)}")
