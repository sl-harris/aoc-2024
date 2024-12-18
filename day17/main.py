from util.files import read_file


def parse_input(input):
    a = int(input[0].replace("Register A: ", ""))
    b = int(input[1].replace("Register B: ", ""))
    c = int(input[2].replace("Register C: ", ""))
    p = [int(p_) for p_ in input[3].replace("Program: ", "").split(",")]

    return a, b, c, p


def get_combo_op(a, b, c, op):
    if 0 <= op <= 3:
        return op

    if op == 4:
        return a

    if op == 5:
        return b

    if op == 6:
        return c

    return -1


def p0_adv(a, b, c, p, out, pointer):
    combo_op = get_combo_op(a, b, c, p[pointer + 1])
    return a // (2**combo_op), b, c, p, out, pointer + 2


def p1_bxl(a, b, c, p, out, pointer):
    return a, b ^ p[pointer + 1], c, p, out, pointer + 2


def p2_bst(a, b, c, p, out, pointer):
    combo_op = get_combo_op(a, b, c, p[pointer + 1])
    return a, combo_op % 8, c, p, out, pointer + 2


def p3_jnz(a, b, c, p, out, pointer):
    if a == 0:
        return a, b, c, p, out, pointer + 2

    return a, b, c, p, out, p[pointer + 1]


def p4_bxc(a, b, c, p, out, pointer):
    return a, b ^ c, c, p, out, pointer + 2


def p5_out(a, b, c, p, out, pointer):
    combo_op = get_combo_op(a, b, c, p[pointer + 1])
    out += [str(combo_op % 8)]
    return a, b, c, p, out, pointer + 2


def p6_bdv(a, b, c, p, out, pointer):
    combo_op = get_combo_op(a, b, c, p[pointer + 1])
    return a, a // (2**combo_op), c, p, out, pointer + 2


def p7_bdv(a, b, c, p, out, pointer):
    combo_op = get_combo_op(a, b, c, p[pointer + 1])
    return a, b, a // (2**combo_op), p, out, pointer + 2


def run_program(a, b, c, p):
    out = []
    pointer = 0

    while pointer < len(p):
        op = p[pointer]

        if op == 0:
            a, b, c, p, out, pointer = p0_adv(a, b, c, p, out, pointer)
        elif op == 1:
            a, b, c, p, out, pointer = p1_bxl(a, b, c, p, out, pointer)
        elif op == 2:
            a, b, c, p, out, pointer = p2_bst(a, b, c, p, out, pointer)
        elif op == 3:
            a, b, c, p, out, pointer = p3_jnz(a, b, c, p, out, pointer)
        elif op == 4:
            a, b, c, p, out, pointer = p4_bxc(a, b, c, p, out, pointer)
        elif op == 5:
            a, b, c, p, out, pointer = p5_out(a, b, c, p, out, pointer)
        elif op == 6:
            a, b, c, p, out, pointer = p6_bdv(a, b, c, p, out, pointer)
        elif op == 7:
            a, b, c, p, out, pointer = p7_bdv(a, b, c, p, out, pointer)

    return out


def run_series(a_from, a_to, b, c, p):
    return [run_program(a, b, c, p) for a in range(a_from, a_to + 1)]


def remove_built(outputs, built):
    str_built = ",".join(built)

    for idx, output in enumerate(outputs):
        str_out = ",".join(output)
        assert str_out[-len(str_built) :] == str_built or str_built == ""
        str_out = str_out[-len(str_built) - 1 :]
        outputs[idx] = list(str_out)

    return outputs


def get_a_range(indices):
    levels = len(indices)
    range_from = 8**levels

    for level in range(1, len(indices) + 1):
        range_from += (indices[-level]) * (8 ** (levels - level + 1))

    range_from -= 8**levels

    range_end = range_from + 8 - 1

    return range_from, range_end


input = read_file("day17/input2.txt", sep="")

a, b, c, p = parse_input(input)
print(f"Part 1: {run_program(a,b,c,p)}")

building = []
to_build = [str(num) for num in p.copy()]
outputs = run_series(0, 7, b, c, p)

building = [to_build.pop(-1)]
indices = [[idx for idx, output in enumerate(outputs) if output == building]]

while True:
    if not to_build:
        break

    building = [to_build.pop(-1)] + building

    while True:
        if len(indices[0]) != len(building) - 1:
            break

        index = indices.pop(0)
        range_from, range_end = get_a_range(index)
        outputs = run_series(range_from, range_end, b, c, p)

        indices += [
            [idx] + index for idx, output in enumerate(outputs) if output == building
        ]

lowest_a_value = get_a_range(indices[0][1:])[0] + 5
print(f"Part 2: {lowest_a_value}")
