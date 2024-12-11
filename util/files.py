def read_file(filename, sep=" "):
    input = []
    with open(filename) as f:
        while True:
            line = f.readline().replace("\n", "")

            if not line:
                break

            if len(sep) > 0:
                input.append(line.split(sep))
            else:
                input.append(line)

    return input
