from util.files import read_file
from itertools import combinations


def parse_input(input):
    connections = {}

    for comp1, comp2 in input:
        connections.setdefault(comp1, set())
        connections[comp1].add(comp2)

        connections.setdefault(comp2, set())
        connections[comp2].add(comp1)

    return connections


def key_starts_with(conns, starts_with):
    return {k: v for k, v in conns.items() if k[0] == starts_with}


def get_unique_conns(conns, keys):
    combos = []

    for comp_1 in keys:
        comps_1 = conns[comp_1]
        for comp_2 in comps_1:
            comps_2 = conns[comp_2]
            comps = comps_1 & comps_2
            combos += [tuple(sorted((comp_1, comp_2, comp))) for comp in comps]

    return set(combos)


def find_interconnected(conns, keys):
    sets = set()

    queue = []

    for comp_1 in keys:
        for comp_2 in conns[comp_1]:
            common = conns[comp_1] & conns[comp_2]

            if len(common) > 0:
                queue.append([[comp_1, comp_2], conns[comp_1] & conns[comp_2]])
            else:
                sets.add(tuple(sorted([comp_1, comp_2])))

    while True:
        if not queue:
            break

        network, common = queue.pop(0)
        next_comp = next(iter(common))

        comps = conns[next_comp]
        common = common & comps

        network.append(next_comp)

        if len(common) > 0:
            queue.append([network, common])
            continue

        sets.add(tuple(sorted(network)))

    return sets


input = read_file("day23/input.txt", sep="-")
conns = parse_input(input)
starts_t = key_starts_with(conns, "t")
combos = get_unique_conns(conns, starts_t.keys())

print(f"Part 1: {len(combos)}")

interconn = find_interconnected(conns, conns.keys())
max_len = max([len(i) for i in interconn])
max_interconn = [i for i in interconn if len(i) == max_len]

print(f"Part 2: {','.join(max_interconn[0])}")
