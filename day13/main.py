from util.files import read_file

CONST = 10_000_000_000_000


def solve(x, y, x_a, y_a, x_b, y_b):
    b = (y * x_a - y_a * x) / (x_a * y_b - x_b * y_a)
    a = (x - b * x_b) / x_a

    return a, b


def parse_input(input, p2=False):
    input_ = []

    for i in range(len(input) // 3):
        a = (
            input[i * 3]
            .replace("Button A: ", "")
            .replace("X+", "")
            .replace("Y+", "")
            .split(", ")
        )
        b = (
            input[i * 3 + 1]
            .replace("Button B: ", "")
            .replace("X+", "")
            .replace("Y+", "")
            .split(", ")
        )
        p = (
            input[i * 3 + 2]
            .replace("Prize: ", "")
            .replace("X=", "")
            .replace("Y=", "")
            .split(", ")
        )

        input_.append(
            (
                int(p[0]) + CONST if p2 else 0,
                int(p[1]) + CONST if p2 else 0,
                int(a[0]),
                int(a[1]),
                int(b[0]),
                int(b[1]),
            )
        )

    return input_


if __name__ == "__main__":
    input = read_file("day13/input.txt", "", True)
    parsed = parse_input(input)

    output = [solve(*i) for i in parsed]
    output = [o for o in output if not (o[0] % 1 != 0 or o[1] % 1 != 0)]
    output = [o[0] * 3 + o[1] for o in output]

    print(f"Part 1: {sum(output)}")

    parsed = parse_input(input, p2=True)

    output = [solve(*i) for i in parsed]
    output = [o for o in output if not (o[0] % 1 != 0 or o[1] % 1 != 0)]
    output = [o[0] * 3 + o[1] for o in output]

    print(f"Part 2: {sum(output)}")
