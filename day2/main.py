from util.files import read_file


def is_safe(seq):
    delta = [int(num_next) - int(num) for num, num_next in zip(seq[:-1], seq[1:])]

    for d in delta:
        if not 1 <= abs(d) <= 3:
            return False

    first_d_positive = delta[0] > 0

    for d in delta:
        if (d > 0) != first_d_positive:
            return False

    return True


def count_safe_reports(input):
    is_safe_ = []

    for i in input:
        is_safe_.append(is_safe(i))

    return is_safe_


def count_safe_reports_dampened(input):
    is_safe_ = count_safe_reports(input)

    for idx, (flag, input_) in enumerate(zip(is_safe_, input)):
        # If report is already safe, move on
        if flag:
            continue

        # If not, remove the level one by one
        for i in range(len(input_)):
            input_mod = input_[:i] + input_[i + 1 :]
            new_flag = is_safe(input_mod)

            if new_flag:
                is_safe_[idx] = new_flag
                break

    return is_safe_


if __name__ == "__main__":
    input = read_file("day2/input.txt")
    # input = read_file("day2/sample.txt")
    print(f"Part 1: {sum(count_safe_reports(input))}")
    print(f"Part 2: {sum(count_safe_reports_dampened(input))}")
