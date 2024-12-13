def read_file(filename, sep=" ", include_blank=False):
    input = []
    with open(filename) as f:
        while line := f.readline():
            if not include_blank and not line:
                break

            line = line.replace("\n", "")

            if not line:
                continue

            if len(sep) > 0:
                input.append(line.split(sep))
            else:
                input.append(line)

    return input
