from util.files import read_file


def parse_input(input):
    input_ = []

    for line in input:
        for i in line:
            for i_ in i.split(")"):
                if len(i_) < 8:
                    i__ = i_.split(",")
                    if len(i__) == 2:
                        input_.append(i__)

    return input_


def multiply(num1, num2):
    return int(num1) * int(num2)


def calc_mult(input):
    result = []

    for i in input:
        try:
            result.append(multiply(i[0], i[1]))
        except:
            result.append(0)

    return result


def parse_switch(input):
    line = [line.split("don't()")[0] for line in input.split("do()")]
    return "".join(line).split("mul(")


if __name__ == "__main__":
    input = read_file("day3/input.txt", "mul(")
    input = parse_input(input)

    print(f"Part 1: {sum(calc_mult(input))}")

    # input = read_file("day3/input copy.txt", "mul(")
    # input = parse_input(input)

    # print(f"Part 2: {sum(calc_mult(input))}")

    input = read_file("day3/input.txt", "")
    input = "".join(input)
    input = parse_switch(input)
    input = parse_input([input])

    print(f"Part 2: {sum(calc_mult(input))}")
