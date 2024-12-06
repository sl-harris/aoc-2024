from util.files import read_file


def reorder_input(input):
    left = []
    right = []

    for i in input:
        left.append(i[0])
        right.append(i[1])

    left.sort()
    right.sort()

    return left, right


def calc_distances(left, right):
    distances = []

    for l, r in zip(left, right):
        distances.append(abs(int(l) - int(r)))

    return distances


def calc_similarity(left, right):
    scores = {}
    score = 0

    for l in left:
        if l in scores.keys():
            score += int(l) * scores[l]
            continue

        scores[l] = sum([1 if l == r else 0 for r in right])
        score += int(l) * scores[l]

    return score


if __name__ == "__main__":
    input = read_file("day1/input.txt", sep="   ")
    # input = read_file("day1/sample.txt", sep="   ")

    left, right = reorder_input(input)
    distances = calc_distances(left, right)

    print(f"Part 1: {sum(distances)}")
    print(f"Part 2: {calc_similarity(left, right)}")
