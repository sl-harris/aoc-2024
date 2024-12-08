from util.files import read_file

OPS = ["+", "*"]
OPS2 = ["+", "*", "|"]


def find_solution(answer, nums, ops=[], ops_master=OPS):
    if len(nums) == 1:
        return ops if answer == nums[0] else []

    for op in ops_master:
        nums_ = nums.copy()
        nums_.pop(1)

        if op == "+":
            nums_[0] = nums[0] + nums[1]
        elif op == "*":
            nums_[0] = nums[0] * nums[1]
        elif op == "|":
            nums_[0] = int(str(nums[0]) + str(nums[1]))

        if valid_ops := find_solution(answer, nums_, ops + [op], ops_master=ops_master):
            return valid_ops


def find_valid_eqs(input, ops_master=OPS):
    valid = []

    for idx, i in enumerate(input):

        if find_solution(i[0], i[1:], ops_master=ops_master):
            valid.append(i)

    return valid


# 5837217516523 TOO LOW
# 5837374519342
if __name__ == "__main__":
    input = read_file("day7/input.txt", sep=": ")
    input = [[i[0]] + i[1].split(" ") for i in input]
    input = [[int(i_) for i_ in i] for i in input]

    valids = find_valid_eqs(input)
    invalids = [i for i in input if i not in valids]
    sum_1 = sum([v[0] for v in valids])

    print(f"Part 1: {sum_1}")

    more_valids = find_valid_eqs(invalids, ops_master=OPS2)
    sum_2 = sum([v[0] for v in more_valids])
    print(f"Part 2: {sum_1 + sum_2}")
