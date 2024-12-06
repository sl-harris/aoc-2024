from util.files import read_file


def parse_input(input):
    updates, rules = [], {}

    for line in input:
        if line.find(",") > -1:
            updates.append(line.split(","))
            continue

        before, after = line.split("|")

        if before in rules.keys():
            rules[before].append(after)
        else:
            rules[before] = [after]

    return updates, rules


def is_update_valid(update, rules):
    for idx, num in enumerate(update):
        for after in update[idx + 1 :]:
            if idx < len(update) - 1 and (
                num not in rules.keys() or not after in rules[num]
            ):
                return False

    return True


def get_valid_updates(updates, rules):
    return [update for update in updates if is_update_valid(update, rules)]


def get_middle_numbers(valid_updates):
    return [int(update[int(len(update) / 2)]) for update in valid_updates]


def is_after_valid(num, idx, after, update, rules):
    return (idx == len(update) - 1) or (
        (idx < len(update) - 1) and num in rules.keys() and after in rules[num]
    )


def reorder_invalid(invalid_update, rules, reordered=[]):
    if len(invalid_update) == 1:
        return reordered + invalid_update

    for idx, num in enumerate(invalid_update):
        all_afters_valid = all(
            [
                is_after_valid(num, idx, after, invalid_update, rules)
                for after in invalid_update[:idx] + invalid_update[idx + 1 :]
            ]
        )

        if all_afters_valid:
            return reorder_invalid(
                (
                    invalid_update[:idx]
                    + (
                        invalid_update[idx + 1 :]
                        if idx + 1 < len(invalid_update)
                        else []
                    )
                ),
                rules,
                reordered + [num],
            )


def correct_invalid_updates(invalid_updates, rules):
    return [
        reorder_invalid(invalid_update, rules) for invalid_update in invalid_updates
    ]


if __name__ == "__main__":
    input = read_file("day5/input.txt", sep="")

    updates, rules = parse_input(input)
    valid_updates = get_valid_updates(updates, rules)
    middle_numbers = get_middle_numbers(valid_updates)

    print(f"Part 1: {sum(middle_numbers)}")

    invalid_updates = [update for update in updates if update not in valid_updates]
    corrected_updates = correct_invalid_updates(invalid_updates, rules)
    middle_numbers = get_middle_numbers(corrected_updates)

    print(f"Part 2: {sum(middle_numbers)}")
